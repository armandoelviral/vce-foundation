from sp001.infrastructure.inspection_observation_capture_page import (
    install_inspection_observation_capture_page,
)

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from sp001.contracts.retail_inspection_observation import (
    RetailInspectionObservation,
)
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationConflict,
)
from sp001.infrastructure.inspection_observation_read_http_host import (
    create_inspection_observation_read_app,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    deserialize_retail_inspection_observation as deserialize,
    serialize_retail_inspection_observation as serialize,
)
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    InspectionObservationAuthenticationRejected as Rejected,
    InspectionObservationAccessDenied as Denied,
)


def create_inspection_observation_app(
    *, service, max_token_bytes: int = 16384,
    max_request_bytes: int = 1048576,
):
    """Compose read and write routes; no observer attribution is established.

    PUT accepts the canonical observation document as its entire JSON body.
    Limits bound accumulated body bytes, not total server resource use.
    The read-only bootstrap does not automatically enable this factory.
    """
    if not callable(getattr(service, "save", None)):
        raise TypeError("service must provide authenticated saving")
    if type(max_request_bytes) is not int:
        raise TypeError("max_request_bytes must be an integer")
    if max_request_bytes <= 0:
        raise ValueError("max_request_bytes must be positive")
    app = create_inspection_observation_read_app(
        service=service, max_token_bytes=max_token_bytes,
    )

    def response(code, status, **content):
        headers = {
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff",
        }
        if code == 401:
            headers["WWW-Authenticate"] = "Bearer"
        return JSONResponse(
            status_code=code, content={"status": status, **content},
            headers=headers,
        )

    @app.put(
        "/v1/cases/{case_id}/inspection-observations/"
        "{observation_id}/versions/{version}"
    )
    async def save(
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
            token = credential.encode("ascii")
        except UnicodeEncodeError:
            return response(401, "credential_rejected")
        if (
            not token or len(token) > max_token_bytes
            or any(byte < 33 or byte > 126 for byte in token)
        ):
            return response(401, "credential_rejected")
        if (
            request.url.query or not case_id.strip()
            or not version or len(version) > 1000
            or not version.isascii() or not version.isdecimal()
            or version.startswith("0")
        ):
            return response(400, "invalid_request")

        content_types = request.headers.getlist("content-type")
        encodings = request.headers.getlist("content-encoding")
        if (
            len(content_types) != 1
            or content_types[0].split(";", 1)[0].strip().lower()
            != "application/json"
            or (encodings and (
                len(encodings) != 1 or encodings[0].lower() != "identity"
            ))
        ):
            return response(415, "unsupported_content")

        body = bytearray()
        try:
            async for chunk in request.stream():
                if len(body) + len(chunk) > max_request_bytes:
                    return response(413, "request_too_large")
                body.extend(chunk)
        except Exception:
            return response(400, "invalid_request")

        try:
            document = body.decode("utf-8")
            observation = deserialize(document)
            if (
                observation.case_id != case_id
                or observation.observation_id != observation_id
                or observation.observation_version != int(version)
            ):
                return response(400, "invalid_request")
        except (ValueError, TypeError, UnicodeError, RecursionError):
            return response(400, "invalid_request")

        try:
            confirmed = await run_in_threadpool(
                service.save, credential=credential, observation=observation,
            )
            if (
                type(confirmed) is not RetailInspectionObservation
                or serialize(confirmed) != document
            ):
                raise ValueError("inconsistent save confirmation")
        except Rejected:
            return response(
                401, "credential_rejected", save_outcome="unconfirmed",
            )
        except Denied:
            return response(
                403, "access_denied", save_outcome="unconfirmed",
            )
        except RetailInspectionObservationConflict:
            return response(409, "observation_conflict")
        except Exception:
            return response(503, "save_unconfirmed", save_outcome="unconfirmed")

        return response(
            200, "saved", observation_id=observation_id,
            observation_version=version,
        )

    install_inspection_observation_capture_page(app)
    return app
