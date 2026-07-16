import json
from pathlib import Path


REGISTRY = Path(
    "research/conformance/CAPABILITY_REGISTRY.json"
)

TRACEABILITY = Path(
    "research/specifications/TRACEABILITY.yaml"
)


def registry():
    return json.loads(
        REGISTRY.read_text(
            encoding="utf-8",
        )
    )


def traceability() -> str:
    return TRACEABILITY.read_text(
        encoding="utf-8",
    )


def test_every_registered_claim_is_traced() -> None:
    traced = traceability()

    for capability in registry()["capabilities"].values():
        for claim in capability["claims"]:
            assert claim in traced


def test_every_capability_references_claims() -> None:
    for capability in registry()["capabilities"].values():
        assert capability["claims"]


def test_claim_registry_is_not_empty() -> None:
    capabilities = registry()["capabilities"]

    claims = {
        claim
        for capability in capabilities.values()
        for claim in capability["claims"]
    }

    assert claims
