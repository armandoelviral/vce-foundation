import json
import re

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from sp001.contracts.case_access_context import CaseAccessOperation
from sp001.contracts.case_access_issuance_request import (
    CaseAccessIssuanceRequest, IssuanceRequestConflictError,
)
from sp001.infrastructure.jwt_case_access_authenticator import AccessTokenKeyResolutionError
from sp001.services.authenticated_case_access_issuance import (
    AuthenticatedCaseAccessIssuance, IssuanceAuthenticationRejected,
)
from sp001.services.case_access_issuance_reference_validation import (
    IssuanceReferenceValidationError,
)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON member")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("invalid JSON constant")


def create_case_access_issuer_app(
    *, service: AuthenticatedCaseAccessIssuance,
    max_request_bytes: int, max_primary_credential_bytes: int,
) -> FastAPI:
    if not isinstance(service, AuthenticatedCaseAccessIssuance):
        raise TypeError("service must be an AuthenticatedCaseAccessIssuance")
    for value in (max_request_bytes, max_primary_credential_bytes):
        if type(value) is not int or value <= 0:
            raise ValueError("request limits must be positive integers")

    app = FastAPI(
        docs_url=None, redoc_url=None, openapi_url=None, redirect_slashes=False,
    )

    def error(status, code):
        headers = {"Cache-Control": "no-store", "Pragma": "no-cache"}
        if status == 401:
            headers["WWW-Authenticate"] = "Bearer"
        return JSONResponse(
            {"version": "sp001.case-access-issuance.v1", "code": code},
            status_code=status, headers=headers,
        )

    @app.post("/v1/case-access-token")
    async def issue(request: Request):
        authorization = request.headers.getlist("authorization")
        if len(authorization) != 1:
            return error(401, "PRIMARY_CREDENTIAL_REJECTED")
        match = re.fullmatch(
            r"Bearer ([A-Za-z0-9\-._~+/]+=*)", authorization[0], flags=re.IGNORECASE,
        )
        if match is None:
            return error(401, "PRIMARY_CREDENTIAL_REJECTED")
        credential = match.group(1)
        if len(credential.encode("ascii")) > max_primary_credential_bytes:
            return error(401, "PRIMARY_CREDENTIAL_REJECTED")
        if request.url.query:
            return error(400, "INVALID_REQUEST")
        content_types = request.headers.getlist("content-type")
        if (
            len(content_types) != 1
            or content_types[0].split(";", 1)[0].strip().lower() != "application/json"
            or request.headers.get("content-encoding", "identity") != "identity"
        ):
            return error(415, "UNSUPPORTED_CONTENT")
        body = bytearray()
        async for chunk in request.stream():
            if len(body) + len(chunk) > max_request_bytes:
                return error(413, "REQUEST_TOO_LARGE")
            body.extend(chunk)
        try:
            value = json.loads(
                body.decode("utf-8"), object_pairs_hook=_unique_object,
                parse_constant=_invalid_constant,
            )
            if not isinstance(value, dict) or set(value) != {
                "request_id", "case_id", "operation",
            }:
                return error(400, "INVALID_REQUEST")
            if not isinstance(value["operation"], str):
                return error(400, "INVALID_REQUEST")
            intent = CaseAccessIssuanceRequest(
                value["request_id"], value["case_id"],
                CaseAccessOperation(value["operation"]),
            )
        except (ValueError, TypeError, UnicodeError):
            return error(400, "INVALID_REQUEST")

        def execute():
            service.prepare_request(credential=credential, request=intent)
            return service.complete(
                credential=credential, request_id=intent.request_id,
            )

        try:
            token = await run_in_threadpool(execute)
        except IssuanceAuthenticationRejected:
            return error(401, "PRIMARY_CREDENTIAL_REJECTED")
        except AccessTokenKeyResolutionError:
            return error(503, "KEY_PROVIDER_UNAVAILABLE")
        except IssuanceRequestConflictError:
            return error(409, "ISSUANCE_REQUEST_CONFLICT")
        except (PermissionError, IssuanceReferenceValidationError):
            return error(403, "ISSUANCE_NOT_AUTHORIZED")
        except Exception:
            return error(500, "ISSUANCE_FAILED")
        return JSONResponse(
            {
                "version": "sp001.case-access-issuance.v1",
                "request_id": intent.request_id,
                "token_type": "Bearer",
                "access_token": token.credential,
            },
            headers={"Cache-Control": "no-store", "Pragma": "no-cache"},
        )

    return app
