"""BLOCKER-HOST-001: fail-closed PRODUCT-001 startup policy.

This module evaluates startup eligibility. It does not
itself prevent a host from opening network listeners.
"""

BLOCKER_HOST_001_OPEN = True

COMMERCIAL_ENVIRONMENTS = frozenset({
    "production",
    "commercial",
    "staging-commercial",
})


class CommercialStartupBlockedError(RuntimeError):
    """PRODUCT-001 commercial startup is prohibited."""


def authorize_product001_startup(
    *,
    environment: str,
    trust_root_verified: bool,
) -> bool:
    """Authorize laboratory startup only while blocker is open."""

    if not isinstance(environment, str):
        raise TypeError("environment must be a string")

    if not isinstance(trust_root_verified, bool):
        raise TypeError(
            "trust_root_verified must be a boolean"
        )

    if environment == "laboratory":
        return True

    if environment in COMMERCIAL_ENVIRONMENTS:
        if BLOCKER_HOST_001_OPEN:
            raise CommercialStartupBlockedError(
                "BLOCKER-HOST-001 remains open: "
                "commercial startup prohibited"
            )

        if not trust_root_verified:
            raise CommercialStartupBlockedError(
                "verified external trust root required"
            )

        return True

    raise CommercialStartupBlockedError(
        "unknown PRODUCT-001 environment"
    )
