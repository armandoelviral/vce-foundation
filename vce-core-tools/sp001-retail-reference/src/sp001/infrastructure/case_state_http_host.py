from sp001.infrastructure.case_state_http_route import (
    CASE_STATE_ROUTE, validate_case_path_id,
)
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from sp001.contracts.case_state_reader import CaseStateReader
from sp001.contracts.case_state_read_result import Found, NotFound


CONTRACT_VERSION = "sp001.case-state.v1"
AccessPolicy = Callable[[Request, str], bool]


def create_case_state_app(
    *,
    reader: CaseStateReader,
    authorize: AccessPolicy,
) -> FastAPI:
    """Compose an HTTP host; authentication policy is supplied by the caller."""
    if not isinstance(reader, CaseStateReader):
        raise TypeError("reader must implement CaseStateReader")
    if not callable(authorize):
        raise TypeError("authorize must be callable")

    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        redirect_slashes=False,
    )

    def error(status: int, code: str) -> JSONResponse:
        return JSONResponse(
            status_code=status,
            content={"contract_version": CONTRACT_VERSION, "code": code},
            headers={"Cache-Control": "no-store"},
        )

    @app.get(CASE_STATE_ROUTE)
    def read_case_state(request: Request, caseId: str) -> JSONResponse:
        if request.scope["query_string"]:
            return error(400, "INVALID_REQUEST")
        case_id = caseId
        try:
            validate_case_path_id(case_id)
        except (TypeError, ValueError):
            return error(400, "INVALID_REQUEST")

        try:
            allowed = authorize(request, case_id)
        except Exception:
            return error(500, "ACCESS_POLICY_FAILED")
        if allowed is False:
            return error(403, "ACCESS_DENIED")
        if allowed is not True:
            return error(500, "INVALID_ACCESS_DECISION")

        try:
            result = reader.read(case_id=case_id)
            if isinstance(result, NotFound):
                if result.case_id != case_id:
                    return error(502, "INVALID_READER_RESPONSE")
                return JSONResponse(
                    status_code=404,
                    content={
                        "contract_version": CONTRACT_VERSION,
                        "code": "CASE_NOT_FOUND",
                        "case_id": case_id,
                    },
                    headers={"Cache-Control": "no-store"},
                )
            if not isinstance(result, Found):
                return error(502, "INVALID_READER_RESPONSE")
            state = result.state
            if state.case_id != case_id:
                return error(502, "INVALID_READER_RESPONSE")
            payload = {
                "contract_version": CONTRACT_VERSION,
                "code": "CASE_FOUND",
                "case_id": case_id,
                "state": {
                    "case_id": state.case_id,
                    "objective_id": state.objective_id,
                    "scope": state.scope,
                    "phase": state.phase.value,
                    "revision": state.revision,
                    "resource_links": [
                        {
                            "relationship": link.relationship,
                            "resource_type": link.resource_type,
                            "resource_id": link.resource_id,
                        }
                        for link in state.resource_links
                    ],
                },
            }
            return JSONResponse(
                status_code=200,
                content=payload,
                headers={"Cache-Control": "no-store"},
            )
        except Exception:
            # Never expose local exception details or claim domain absence.
            return error(500, "CASE_READ_FAILED")

    return app
