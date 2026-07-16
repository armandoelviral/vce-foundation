import json
from pathlib import Path
from typing import Any


REGISTRY = Path(
    "research/conformance/CAPABILITY_REGISTRY.json"
)

TRACEABILITY = Path(
    "research/specifications/TRACEABILITY.yaml"
)


def registry() -> dict[str, Any]:
    return json.loads(
        REGISTRY.read_text(
            encoding="utf-8",
        )
    )


def traceability_text() -> str:
    return TRACEABILITY.read_text(
        encoding="utf-8",
    )


def test_capability_registry_exists() -> None:
    assert REGISTRY.is_file()


def test_capability_registry_is_valid_json() -> None:
    data = registry()

    assert isinstance(data, dict)
    assert data["version"] == 1


def test_capability_ids_are_unique() -> None:
    capabilities = registry()["capabilities"]

    assert len(capabilities) == len(
        set(capabilities)
    )


def test_every_capability_has_required_fields() -> None:
    capabilities = registry()["capabilities"]

    assert capabilities

    for capability_id, capability in capabilities.items():
        assert capability_id.startswith("CAP-")
        assert capability["name"]
        assert capability["claims"]
        assert capability["contracts"]


def test_every_registered_claim_exists_in_traceability() -> None:
    traceability = traceability_text()

    for capability in registry()["capabilities"].values():
        for claim_id in capability["claims"]:
            assert claim_id in traceability, claim_id


def test_every_registered_contract_exists() -> None:
    for capability in registry()["capabilities"].values():
        for contract in capability["contracts"]:
            assert Path(contract).is_file(), contract


def test_registry_contains_traced_capabilities() -> None:
    names = {
        capability["name"]
        for capability in registry()["capabilities"].values()
    }

    assert names == {
        "Knowledge Lifecycle",
        "Replay Determinism",
    }
