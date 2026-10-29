from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from sp001.contracts.retail_inspection_observation import (
    RetailInspectionObservation,
)
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationIdentity,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    InspectionObservationAuthenticationRejected as Rejected,
    InspectionObservationAccessDenied as Denied,
)


def create_inspection_observation_read_app(
    *, service, max_token_bytes: int = 16384,
) -> FastAPI:
    """Expose exact-version recovery through an authenticated service.

    No credential, backend exception detail or observation is returned on errors.
    Final reauthorization does not eliminate the network-delivery race.
    """
    if not callable(getattr(service, "recover", None)):
        raise TypeError("service must provide authenticated recovery")
    if type(max_token_bytes) is not int:
        raise TypeError("max_token_bytes must be an integer")
    if max_token_bytes <= 0:
        raise ValueError("max_token_bytes must be positive")

    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    def response(status_code, status, **content):
        headers = {
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff",
        }
        if status_code == 401:
            headers["WWW-Authenticate"] = "Bearer"
        return JSONResponse(
            status_code=status_code,
            content={"status": status, **content},
            headers=headers,
        )

    def document_for(observation, identity, case_id):
        if type(observation) is not RetailInspectionObservation:
            raise TypeError("service returned an invalid observation")
        if observation.case_id != case_id:
            raise Denied("observation access denied")
        if (
            observation.observation_id != identity.observation_id
            or observation.observation_version != identity.observation_version
        ):
            raise ValueError("service returned another observation identity")
        return serialize(observation)

    @app.get(
        "/v1/cases/{case_id}/inspection-observations/"
        "{observation_id}/versions/{version}"
    )
    def recover(
        request: Request, case_id: str, observation_id: str, version: str,
    ):
        authorization = request.headers.getlist("authorization")
        if len(authorization) != 1:
            return response(401, "credential_rejected")
        parts = authorization[0].split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return response(401, "credential_rejected")
        credential = parts[1]
        try:
            token_bytes = credential.encode("ascii")
        except UnicodeEncodeError:
            return response(401, "credential_rejected")
        if (
            not token_bytes or len(token_bytes) > max_token_bytes
            or any(byte < 33 or byte > 126 for byte in token_bytes)
        ):
            return response(401, "credential_rejected")

        # Bound integer parsing; version uses a canonical positive decimal.
        if (
            not version or len(version) > 1000
            or not version.isascii() or not version.isdecimal()
            or version.startswith("0")
        ):
            return response(400, "invalid_request")
        try:
            identity = RetailInspectionObservationIdentity(
                observation_id, int(version),
            )
            if not case_id.strip():
                return response(400, "invalid_request")
        except (ValueError, TypeError):
            return response(400, "invalid_request")

        try:
            observation = service.recover(
                credential=credential, identity=identity, case_id=case_id,
            )
            if observation is None:
                return response(404, "observation_not_found")

            document = document_for(observation, identity, case_id)
            confirmed = service.recover(
                credential=credential, identity=identity, case_id=case_id,
            )
            if confirmed is None:
                raise ValueError("observation disappeared during preparation")
            if document_for(confirmed, identity, case_id) != document:
                raise ValueError("observation changed during preparation")
            return response(200, "ok", observation_document=document)
        except Rejected:
            return response(401, "credential_rejected")
        except Denied:
            return response(403, "access_denied")
        except Exception:
            return response(503, "backend_unavailable")

    return app
