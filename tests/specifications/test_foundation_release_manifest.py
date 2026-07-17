import json
from pathlib import Path
from typing import Any


MANIFEST = Path(
    "research/releases/"
    "HAS_FOUNDATION_1_0_MANIFEST.json"
)

REQUIRED_PLATFORMS = {
    "Runtime",
    "Executable Knowledge Infrastructure",
    "Specification Platform",
    "Conformance Platform",
}

REQUIRED_RELEASE_GATES = {
    "runtime",
    "specifications",
    "conformance",
    "foundation",
}


def manifest() -> dict[str, Any]:
    return json.loads(
        MANIFEST.read_text(
            encoding="utf-8",
        )
    )


def test_release_manifest_exists() -> None:
    assert MANIFEST.is_file()


def test_release_manifest_is_valid_json() -> None:
    data = manifest()

    assert isinstance(data, dict)
    assert data["schema_version"] == 1


def test_release_identity_is_frozen_lts_1_0() -> None:
    release = manifest()["release"]

    assert release == {
        "name": "HAS Foundation",
        "version": "1.0",
        "status": "Frozen",
        "channel": "LTS",
    }


def test_manifest_declares_required_platforms() -> None:
    platforms = set(
        manifest()["platforms"]
    )

    assert platforms == REQUIRED_PLATFORMS


def test_every_normative_asset_exists() -> None:
    assets = manifest()["normative_assets"]

    assert assets

    for asset in assets:
        assert Path(asset).is_file(), asset


def test_every_closure_contract_exists() -> None:
    contracts = manifest()["closure_contracts"]

    assert contracts

    for contract in contracts:
        assert Path(contract).is_file(), contract


def test_manifest_declares_release_gates() -> None:
    release_gates = manifest()["release_gates"]

    assert set(release_gates) == REQUIRED_RELEASE_GATES

    assert Path(
        release_gates["runtime"]
    ).is_dir()

    assert Path(
        release_gates["specifications"]
    ).is_dir()

    assert Path(
        release_gates["conformance"]
    ).is_dir()

    for suite in release_gates["foundation"]:
        assert Path(suite).is_dir(), suite


def test_manifest_declares_next_milestone() -> None:
    next_milestone = manifest()["next_milestone"]

    assert next_milestone["id"] == "SR-001"

    assert (
        next_milestone["name"]
        == "Specification Runtime Charter"
    )
