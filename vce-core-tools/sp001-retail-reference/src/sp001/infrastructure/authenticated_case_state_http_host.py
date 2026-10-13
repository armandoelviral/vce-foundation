import re
import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from sp001.contracts.case_access_context import (
    CaseAccessContextAuthenticator,
    CaseAccessContextAuthorizer,
    CaseAccessOperation,
    CaseAccessPermission,
    ValidatedCaseAccessContext,
)
from sp001.contracts.case_state_reader import CaseStateReader
from sp001.infrastructure.case_state_http_host import (
    CONTRACT_VERSION,
    create_case_state_app,
)


_BEARER = re.compile(r"Bearer ([A-Za-z0-9._~+/-]+=*)", re.IGNORECASE)


def create_authenticated_case_state_app(
    *,
    reader: CaseStateReader,
    authenticator: CaseAccessContextAuthenticator,
    authorizer: CaseAccessContextAuthorizer,
    expected_audience: str,
):
    if not isinstance(authenticator, CaseAccessContextAuthenticator):
        raise TypeError("authenticator must implement CaseAccessContextAuthenticator")
    if not isinstance(authorizer, CaseAccessContextAuthorizer):
        raise TypeError("authorizer must implement CaseAccessContextAuthorizer")
    if not isinstance(expected_audience, str):
        raise TypeError("expected_audience must be a string")
    if not expected_audience.strip():
        raise ValueError("expected_audience must not be empty")

    def usable(access: ValidatedCaseAccessContext) -> bool:
        now = time.time()
        return (
            access.audience == expected_audience
            and access.issued_at <= now
            and access.not_before <= now < access.expires_at
        )

    def authorize(request: Request, case_id: str) -> bool:
        access = getattr(request.state, "case_read_access", None)
        if not isinstance(access, ValidatedCaseAccessContext):
            return False
        # Recheck after middleware; access may expire before endpoint execution.
        if not usable(access):
            return False
        required = CaseAccessPermission(case_id, CaseAccessOperation.READ_STATE)
        if required not in access.permissions:
            return False
        return authorizer.can_read_case(access=access, case_id=case_id)

    app = create_case_state_app(reader=reader, authorize=authorize)

    def failure(status: int, code: str) -> JSONResponse:
        headers = {"Cache-Control": "no-store"}
        if status == 401:
            headers["WWW-Authenticate"] = 'Bearer realm="sp001-case-state"'
        return JSONResponse(
            status_code=status,
            content={"contract_version": CONTRACT_VERSION, "code": code},
            headers=headers,
        )

    @app.middleware("http")
    async def authenticate_request(request: Request, call_next):
        if request.url.path != "/v1/case-state":
            return await call_next(request)
        values = request.headers.getlist("authorization")
        if len(values) != 1:
            return failure(401, "AUTHENTICATION_REQUIRED")
        match = _BEARER.fullmatch(values[0])
        if match is None:
            return failure(401, "INVALID_CREDENTIAL")
        try:
            access = await run_in_threadpool(
                authenticator.authenticate, credential=match.group(1)
            )
        except Exception:
            return failure(500, "AUTHENTICATION_PROVIDER_FAILED")
        if access is None:
            return failure(401, "INVALID_CREDENTIAL")
        if not isinstance(access, ValidatedCaseAccessContext):
            return failure(500, "INVALID_AUTHENTICATION_RESULT")
        if not usable(access):
            return failure(401, "INVALID_ACCESS_CONTEXT")
        request.state.case_read_access = access
        return await call_next(request)

    return app
