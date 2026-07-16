import json
from pathlib import Path
from typing import Any


RELEASE = Path(
    "research/releases/HAS_FOUNDATION_1_0.json"
)


def release() -> dict[str, Any]:
    return json.loads(
        RELEASE.read_text(
            encoding="utf-8",
        )
    )


def test_release_registry_exists() -> None:
    assert RELEASE.is_file()


def test_release_registry_is_valid_json() -> None:
    data = release()

    assert isinstance(data, dict)


def test_release_identity_is_frozen_foundation_1_0() -> None:
    data = release()["release"]

    assert data["name"] == "HAS Foundation"
    assert data["version"] == "1.0"
    assert data["status"] == "Frozen"


def test_every_registered_asset_exists() -> None:
    assets = release()["assets"]["specifications"]

    assert assets

    for asset in assets:
        assert Path(asset).is_file(), asset


def test_every_registered_contract_exists() -> None:
    contracts = release()["contracts"]["specification"]

    assert contracts

    for contract in contracts:
        assert Path(contract).is_file(), contract


def test_registered_suites_exist() -> None:
    suites = release()["suites"]

    assert Path(suites["runtime"]).is_dir()
    assert Path(suites["specifications"]).is_dir()
