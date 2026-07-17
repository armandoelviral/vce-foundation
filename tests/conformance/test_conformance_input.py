from dataclasses import FrozenInstanceError

import pytest

from has.conformance.model.conformance_input import (
    ConformanceInput,
)


def test_input_is_immutable() -> None:
    model = ConformanceInput(
        claim="KS-001",
        capability="Knowledge Lifecycle",
        executable_contract="contract.py",
        coverage_status="Covered",
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        model.claim = "OTHER"


def test_input_reports_covered() -> None:
    model = ConformanceInput(
        claim="KS-001",
        capability="Knowledge Lifecycle",
        executable_contract="contract.py",
        coverage_status="Covered",
    )

    assert model.is_covered()


def test_input_reports_not_covered() -> None:
    model = ConformanceInput(
        claim="KS-001",
        capability="Knowledge Lifecycle",
        executable_contract="contract.py",
        coverage_status="Not Covered",
    )

    assert not model.is_covered()


def test_input_preserves_values() -> None:
    model = ConformanceInput(
        claim="GP-001",
        capability="Replay Determinism",
        executable_contract="runtime.py",
        coverage_status="Covered",
    )

    assert model.claim == "GP-001"

    assert (
        model.capability
        == "Replay Determinism"
    )

    assert (
        model.executable_contract
        == "runtime.py"
    )
