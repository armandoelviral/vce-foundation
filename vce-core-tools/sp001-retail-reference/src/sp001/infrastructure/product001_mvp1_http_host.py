"""PRODUCT-001 MVP1 protected laboratory HTTP host."""

import asyncio
from base64 import b64encode
from collections.abc import Callable
from dataclasses import asdict

from fastapi import FastAPI, HTTPException, Request
from starlette.concurrency import run_in_threadpool

from sp001.contracts.product001_mvp1_commercial_receipt import CommercialReceiptV1
from sp001.infrastructure.product001_mvp1_commercial_evidence import CommercialEvidenceStatus
from sp001.services.product001_mvp1_commercial_receipt_issuer import Mvp1CommercialReceiptIssuer
from sp001.infrastructure.product001_mvp1_http_composition import (
    read_product001_mvp1_commitment_request,
)
from sp001.infrastructure.product001_mvp1_protected_composition import (
    Product001MVP1ProtectedApproval,
)
from sp001.infrastructure.sqlite_product001_commercial_decisions import (
    CommercialDecisionConflict,
)


def create_product001_mvp1_http_app(
    *,
    protected_service: Product001MVP1ProtectedApproval,
    enable_commitment_route: bool = False,
    receipt_issuer: Mvp1CommercialReceiptIssuer | None = None,
    after_commit: Callable[[], None] | None = None,
) -> FastAPI:
    """Expose the laboratory route only with trusted opt-in and certificate mode."""
    if not isinstance(protected_service, Product001MVP1ProtectedApproval):
        raise TypeError("protected approval service required")
    if type(enable_commitment_route) is not bool:
        raise TypeError("invalid commitment route configuration")
    if enable_commitment_route and not protected_service.requires_commitment_certificate:
        raise ValueError("commitment route requires certificate admission")

    if receipt_issuer is not None and (
        not enable_commitment_route or not isinstance(receipt_issuer, Mvp1CommercialReceiptIssuer)
    ):
        raise TypeError("receipt delivery requires the protected commitment route and issuer")
    if after_commit is not None and (receipt_issuer is None or not callable(after_commit)):
        raise TypeError("post-commit hook requires receipt delivery")

    app = FastAPI(
        title="PRODUCT-001 MVP1 Protected Laboratory Host",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        redirect_slashes=False,
    )
    if not enable_commitment_route:
        return app

    async def read_request(request: Request):
        credentials = request.headers.getlist("authorization")
        if len(credentials) != 1:
            raise HTTPException(status_code=401, detail="Bearer credential required")
        scheme, _, credential = credentials[0].partition(" ")
        if scheme.lower() != "bearer" or not credential or any(
            char.isspace() or char == "," for char in credential
        ):
            raise HTTPException(status_code=401, detail="Bearer credential required")

        lengths = request.headers.getlist("content-length")
        if len(lengths) > 1:
            raise HTTPException(status_code=400, detail="Invalid Content-Length")
        try:
            async with asyncio.timeout(5):
                decision, certificate = await read_product001_mvp1_commitment_request(
                    request.receive, content_length=lengths[0] if lengths else None,
                )
        except TimeoutError as error:
            raise HTTPException(status_code=408, detail="Request body timeout") from error
        except (TypeError, ValueError) as error:
            raise HTTPException(status_code=400, detail="Invalid commitment request") from error

        return credential, decision, certificate

    def receipt_payload(certificate):
        result = receipt_issuer.recover(certificate)
        if result is CommercialEvidenceStatus.REJECTED:
            raise HTTPException(status_code=403, detail="Receipt evidence rejected")
        if not isinstance(result, CommercialReceiptV1):
            raise HTTPException(status_code=503, detail="Receipt evidence unavailable")
        return {
            "version": 1,
            "statement": asdict(result.statement),
            "signature_b64": b64encode(result.signature).decode("ascii"),
        }

    @app.post("/laboratory/product001/mvp1/decisions")
    async def record_decision(request: Request):
        credential, decision, certificate = await read_request(request)
        try:
            recorded = await run_in_threadpool(
                protected_service.record,
                credential=credential,
                decision=decision,
                authorization=certificate,
            )
        except PermissionError as error:
            raise HTTPException(status_code=403, detail="Admission denied") from error
        except CommercialDecisionConflict as error:
            raise HTTPException(status_code=409, detail="Decision conflict") from error
        response = {"recorded": recorded}
        if receipt_issuer is not None:
            if recorded and after_commit is not None:
                await run_in_threadpool(after_commit)
            response["receipt"] = await run_in_threadpool(receipt_payload, certificate)
        return response

    if receipt_issuer is not None:
        @app.post("/laboratory/product001/mvp1/receipts")
        async def recover_receipt(request: Request):
            credential, decision, certificate = await read_request(request)
            try:
                await run_in_threadpool(
                    protected_service.authenticate_receipt_request,
                    credential=credential,
                    decision=decision,
                    certificate=certificate,
                )
            except PermissionError as error:
                raise HTTPException(status_code=403, detail="Receipt access denied") from error
            return {"receipt": await run_in_threadpool(receipt_payload, certificate)}

    return app
