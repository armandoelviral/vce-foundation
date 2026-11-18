"""PRODUCT-001 protected host bootstrap."""

import os
from collections.abc import Mapping

from fastapi import FastAPI

from sp001.services.product001_commercial_startup_guard import (
    authorize_product001_startup,
)


def create_app_from_environment(
    *,
    environment: Mapping[str, str],
) -> FastAPI:
    mode = environment.get("PRODUCT001_ENV")

    if mode is None:
        from sp001.services.product001_commercial_startup_guard import (
            CommercialStartupBlockedError,
        )
        raise CommercialStartupBlockedError(
            "PRODUCT001_ENV is required for startup"
        )

    # Authorization must precede application construction.
    authorize_product001_startup(
        environment=mode,
        trust_root_verified=False,
    )

    # No commercial endpoints are connected in D2.2.
    return FastAPI(
        title="PRODUCT-001 Laboratory Host"
    )


def create_app() -> FastAPI:
    return create_app_from_environment(
        environment=dict(os.environ)
    )
