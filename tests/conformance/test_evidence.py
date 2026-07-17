from dataclasses import FrozenInstanceError

import pytest

from has.conformance.model.evidence import (
    Evidence,
)


def test_evidence_is_immutable() -> None:
    evidence = Evidence(
        source="pytest",
        status="Available",
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        evidence.source = "other"


def test_available_evidence() -> None:
    evidence = Evidence(
        source="pytest",
        status="Available",
    )

    assert evidence.available


def test_missing_evidence() -> None:
    evidence = Evidence(
        source="pytest",
        status="Missing",
    )

    assert not evidence.available


def test_invalid_status_is_rejected() -> None:
    with pytest.raises(ValueError):
        Evidence(
            source="pytest",
            status="UNKNOWN",
        )


def test_source_is_preserved() -> None:
    evidence = Evidence(
        source="runtime-suite",
        status="Available",
    )

    assert evidence.source == "runtime-suite"
