import json
from pathlib import Path


REGISTRY = Path(
    "research/conformance/CAPABILITY_REGISTRY.json"
)


def registry():
    return json.loads(
        REGISTRY.read_text(
            encoding="utf-8",
        )
    )


def test_every_capability_has_claims() -> None:
    for capability in registry()["capabilities"].values():
        assert capability["claims"]


def test_every_capability_has_contracts() -> None:
    for capability in registry()["capabilities"].values():
        assert capability["contracts"]


def test_every_contract_exists() -> None:
    for capability in registry()["capabilities"].values():

        for contract in capability["contracts"]:

            assert Path(contract).is_file()
