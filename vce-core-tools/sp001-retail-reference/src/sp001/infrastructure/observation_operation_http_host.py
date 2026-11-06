import base64
import binascii
import json
from io import BytesIO

from sp001.infrastructure.observation_operation_read_page import (
    install_observation_operation_read_page,
)

from fastapi import Request
from fastapi.responses import JSONResponse, Response
from starlette.concurrency import run_in_threadpool

from sp001.contracts.retail_observation_operation import (
    RetailObservationSaveRequest as SaveRequest,
    RetailObservationOperationReceipt as Receipt,
    RetailObservationOperationConflict,
)
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationConflict,
)
from sp001.infrastructure.inspection_observation_http_host import (
    create_inspection_observation_app,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    deserialize_retail_inspection_observation as deserialize,
)
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    InspectionObservationAuthenticationRejected as Rejected,
    InspectionObservationAccessDenied as Denied,
)
from sp001.infrastructure.sqlite_observation_operations import (
    ObservationOperationIntegrityFailure,
)
from sp001.services.retail_observation_operation_validation import (
    validate_retail_observation_operation as validate,
)


PHOTO_CONTENT_TYPE = "application/vnd.sp001.observation-photo+json"
MAX_PHOTO_BYTES = 5 * 1024 * 1024
MAX_PHOTO_PIXELS = 20_000_000
MAX_PHOTO_BASE64 = 4 * ((MAX_PHOTO_BYTES + 2) // 3)


class InvalidPhoto(ValueError):
    """The submitted bytes cannot be accepted as a JPEG or PNG."""


def _validate_photo(photo):
    # Import only for photo uploads; legacy JSON operations do not decode images.
    from PIL import Image, UnidentifiedImageError

    try:
        with Image.open(BytesIO(photo), formats=("JPEG", "PNG")) as image:
            if image.width * image.height > MAX_PHOTO_PIXELS:
                raise InvalidPhoto("image exceeds pixel limit")
            if getattr(image, "n_frames", 1) != 1:
                raise InvalidPhoto("animated images are not supported")
            image.verify()
        with Image.open(BytesIO(photo), formats=("JPEG", "PNG")) as image:
            image.load()
    except (UnidentifiedImageError, Image.DecompressionBombError,
            OSError, SyntaxError, ValueError) as error:
        raise InvalidPhoto("invalid or unsupported image") from error


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate envelope field")
        result[key] = value
    return result


def create_observation_operation_app(
    *, service, max_token_bytes=16384, max_request_bytes=1048576,
):
    """Expose authenticated operations; no independent witness or OS isolation.

    saved confirms the backend save response. ok returns a recovered pair.
    Neither constitutes external integrity or inspection authorship.
    Final recovery checks do not eliminate the network-delivery race.
    """
    for name in ("save_operation", "recover_operation"):
        if not callable(getattr(service, name, None)):
            raise TypeError("service must provide authenticated operations")
    app = create_inspection_observation_app(
        service=service, max_token_bytes=max_token_bytes,
        max_request_bytes=max_request_bytes,
        operation_capture=True,
    )

    def response(code, status, **content):
        headers = {
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff",
        }
        if code == 401:
            headers["WWW-Authenticate"] = "Bearer"
        return JSONResponse(
            status_code=code,
            content={"status": status, **content},
            headers=headers,
        )

    def credential_for(request):
        headers = request.headers.getlist("authorization")
        if len(headers) != 1:
            raise Rejected("credential rejected")
        parts = headers[0].split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise Rejected("credential rejected")
        try:
            value = parts[1].encode("ascii")
        except UnicodeEncodeError:
            raise Rejected("credential rejected") from None
        if (
            not value or len(value) > max_token_bytes
            or any(byte < 33 or byte > 126 for byte in value)
        ):
            raise Rejected("credential rejected")
        return parts[1]

    def valid_path(request, case_id, request_id):
        # Reuse the request contract's identifier validation without fabricating
        # an observation: operation identity validates the same request ID.
        from sp001.contracts.case_read_access import AuthenticatedPrincipal
        from sp001.contracts.retail_observation_operation import (
            RetailObservationOperationIdentity,
        )
        if request.url.query:
            return False
        try:
            # This value only validates syntax; it grants no authority.
            RetailObservationOperationIdentity(
                AuthenticatedPrincipal("syntax", "syntax"), case_id, request_id,
            )
        except (TypeError, ValueError):
            return False
        return True

    def receipt_content(receipt, case_id, request_id, expected=None):
        if type(receipt) is not Receipt:
            raise ObservationOperationIntegrityFailure("invalid receipt")
        if (
            receipt.operation.case_id != case_id
            or receipt.operation.request_id != request_id
        ):
            raise ObservationOperationIntegrityFailure("wrong operation")
        try:
            item = deserialize(receipt.stored_observation.document)
            intent = SaveRequest(request_id, item if expected is None else expected)
            validate(
                request=intent, receipt=receipt,
                principal=receipt.operation.principal,
            )
        except (ValueError, TypeError, UnicodeError, RecursionError) as error:
            raise ObservationOperationIntegrityFailure(
                "invalid receipt correspondence"
            ) from error
        return {
            "request_id": request_id,
            "case_id": case_id,
            "observation_id": item.observation_id,
            "observation_version": str(item.observation_version),
            "disposition": receipt.disposition.value,
            "observation_document": receipt.stored_observation.document,
        }

    route = "/v1/cases/{case_id}/inspection-observation-operations/{request_id}"

    @app.put(route)
    async def save(request: Request, case_id: str, request_id: str):
        try:
            credential = credential_for(request)
        except Rejected:
            return response(401, "credential_rejected")
        if not valid_path(request, case_id, request_id):
            return response(400, "invalid_request")
        types = request.headers.getlist("content-type")
        encodings = request.headers.getlist("content-encoding")
        media_type = (
            types[0].split(";", 1)[0].strip().lower() if len(types) == 1 else ""
        )
        with_photo = media_type == PHOTO_CONTENT_TYPE
        if (
            media_type not in ("application/json", PHOTO_CONTENT_TYPE)
            or (encodings and (
                len(encodings) != 1 or encodings[0].lower() != "identity"
            ))
        ):
            return response(415, "unsupported_content")
        body = bytearray()
        photo = None
        limit = max_request_bytes
        if with_photo:
            # Allow escaped JSON text plus the bounded base64 field.
            limit = 6 * max_request_bytes + MAX_PHOTO_BASE64 + 256
        try:
            async for chunk in request.stream():
                if len(body) + len(chunk) > limit:
                    return response(413, "request_too_large")
                body.extend(chunk)
            document = body.decode("utf-8")
            if with_photo:
                envelope = json.loads(document, object_pairs_hook=_unique_object)
                if type(envelope) is not dict or set(envelope) != {
                    "observation_document", "photo_base64",
                }:
                    return response(400, "invalid_request")
                document = envelope["observation_document"]
                encoded = envelope["photo_base64"]
                if type(document) is not str or type(encoded) is not str:
                    return response(400, "invalid_request")
                if (
                    len(document.encode("utf-8")) > max_request_bytes
                    or len(encoded) > MAX_PHOTO_BASE64
                ):
                    return response(413, "request_too_large")
                try:
                    photo = base64.b64decode(encoded, validate=True)
                except (binascii.Error, ValueError):
                    return response(400, "invalid_photo")
                if not photo:
                    return response(400, "invalid_photo")
                if len(photo) > MAX_PHOTO_BYTES:
                    return response(413, "request_too_large")
            item = deserialize(document)
            if item.case_id != case_id:
                return response(400, "invalid_request")
            intent = SaveRequest(request_id, item)
        except (ValueError, TypeError, UnicodeError, RecursionError):
            return response(400, "invalid_request")
        except Exception:
            return response(400, "invalid_request")

        try:
            options = {}
            if photo is not None:
                await run_in_threadpool(_validate_photo, photo)
                options["photo"] = photo
            receipt = await run_in_threadpool(
                service.save_operation, credential=credential, request=intent,
                **options,
            )
            content = receipt_content(receipt, case_id, request_id, item)
            # Save permission does not implicitly authorize document retrieval.
            content.pop("observation_document")
            return response(200, "saved", **content)
        except InvalidPhoto:
            return response(400, "invalid_photo")
        except Rejected:
            return response(401, "credential_rejected", save_outcome="unconfirmed")
        except Denied:
            return response(403, "access_denied", save_outcome="unconfirmed")
        except RetailObservationOperationConflict:
            return response(409, "operation_conflict")
        except RetailInspectionObservationConflict:
            return response(409, "observation_conflict")
        except ObservationOperationIntegrityFailure:
            return response(503, "integrity_failure", save_outcome="unconfirmed")
        except Exception:
            return response(503, "save_unconfirmed", save_outcome="unconfirmed")

    @app.get(route)
    def recover(request: Request, case_id: str, request_id: str):
        try:
            credential = credential_for(request)
        except Rejected:
            return response(401, "credential_rejected")
        if not valid_path(request, case_id, request_id):
            return response(400, "invalid_request")
        try:
            receipt = service.recover_operation(
                credential=credential, case_id=case_id, request_id=request_id,
            )
            if receipt is None:
                return response(404, "operation_not_found")
            content = receipt_content(receipt, case_id, request_id)
            confirmed = service.recover_operation(
                credential=credential, case_id=case_id, request_id=request_id,
            )
            if confirmed != receipt:
                raise ObservationOperationIntegrityFailure(
                    "operation changed during response preparation"
                )
            return response(200, "ok", **content)
        except Rejected:
            return response(401, "credential_rejected")
        except Denied:
            return response(403, "access_denied")
        except ObservationOperationIntegrityFailure:
            return response(503, "integrity_failure")
        except Exception:
            return response(503, "backend_unavailable")

    @app.get(route + "/photo")
    def recover_photo(request: Request, case_id: str, request_id: str):
        try:
            credential = credential_for(request)
        except Rejected:
            return response(401, "credential_rejected")
        if not valid_path(request, case_id, request_id):
            return response(400, "invalid_request")
        try:
            arguments = {
                "credential": credential, "case_id": case_id,
                "request_id": request_id, "include_photo": True,
            }
            result = service.recover_operation(**arguments)
            if result is None:
                return response(404, "operation_not_found")
            receipt, photo = result
            receipt_content(receipt, case_id, request_id)
            if photo is None:
                return response(404, "photo_not_found")
            if service.recover_operation(**arguments) != result:
                raise ObservationOperationIntegrityFailure(
                    "operation changed during photo response preparation"
                )
            return Response(
                content=photo, media_type="application/octet-stream",
                headers={
                    "Content-Disposition": 'attachment; filename="observation-photo"',
                    "Cache-Control": "no-store",
                    "X-Content-Type-Options": "nosniff",
                },
            )
        except Rejected:
            return response(401, "credential_rejected")
        except Denied:
            return response(403, "access_denied")
        except ObservationOperationIntegrityFailure:
            return response(503, "integrity_failure")
        except Exception:
            return response(503, "backend_unavailable")

    install_observation_operation_read_page(app)
    return app
