from fastapi import FastAPI

from sp001.infrastructure.case_access_issuer_composition import compose_case_access_issuer
from sp001.infrastructure.case_access_issuer_http_host import create_case_access_issuer_app


def compose_case_access_issuer_host(
    *, max_request_bytes: int, max_primary_credential_bytes: int,
    **issuer_configuration,
) -> FastAPI:
    for value in (max_request_bytes, max_primary_credential_bytes):
        if type(value) is not int or value <= 0:
            raise ValueError("HTTP limits must be positive integers")
    service = compose_case_access_issuer(**issuer_configuration)
    return create_case_access_issuer_app(
        service=service, max_request_bytes=max_request_bytes,
        max_primary_credential_bytes=max_primary_credential_bytes,
    )
