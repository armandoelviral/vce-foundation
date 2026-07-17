from dataclasses import FrozenInstanceError

import pytest

from has.conformance.model.decision import Decision
from has.conformance.model.decision_record import DecisionRecord
from has.conformance.model.evidence import Evidence


def available_evidence() -> Evidence:
    return Evidence(
        source="runtime-suite",
        status="Available",
    )


def missing_evidence() -> Evidence:
    return Evidence(
        source="runtime-suite",
        status="Missing",
    )


def test_conformant_record() -> None:
    record = DecisionRecord(
        claim="GP-001",
        capability="Replay Determinism",
        executable_contract=(
            "tests/runtime/invariants/"
            "test_invariant_replay_determinism.py"
        ),
        coverage_status="Covered",
        decision=Decision.CONFORMANT,
        evidence=available_evidence(),
    )

    assert record.conformant
    assert record.failure_reason is None


def test_non_conformant_record_accepts_failure_reason() -> None:
    record = DecisionRecord(
        claim="GP-001",
        capability="Replay Determinism",
        executable_contract=(
            "tests/runtime/invariants/"
            "test_invariant_replay_determinism.py"
        ),
        coverage_status="Not Covered",
        decision=Decision.NON_CONFORMANT,
        evidence=missing_evidence(),
        failure_reason="missing_evidence",
    )

    assert not record.conformant
    assert record.failure_reason == "missing_evidence"


def test_record_is_immutable() -> None:
    record = DecisionRecord(
        claim="GP-001",
        capability="Replay Determinism",
        executable_contract="contract.py",
        coverage_status="Covered",
        decision=Decision.CONFORMANT,
        evidence=available_evidence(),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        record.claim = "OTHER"


def test_conformant_record_rejects_failure_reason() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "conformant decision cannot contain "
            "a failure reason"
        ),
    ):
        DecisionRecord(
            claim="GP-001",
            capability="Replay Determinism",
            executable_contract="contract.py",
            coverage_status="Covered",
            decision=Decision.CONFORMANT,
            evidence=available_evidence(),
            failure_reason="unexpected",
        )


def test_conformant_record_requires_available_evidence() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "conformant decision requires "
            "available evidence"
        ),
    ):
        DecisionRecord(
            claim="GP-001",
            capability="Replay Determinism",
            executable_contract="contract.py",
            coverage_status="Covered",
            decision=Decision.CONFORMANT,
            evidence=missing_evidence(),
        )


def test_conformant_record_requires_covered_status() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "conformant decision requires "
            "covered status"
        ),
    ):
        DecisionRecord(
            claim="GP-001",
            capability="Replay Determinism",
            executable_contract="contract.py",
            coverage_status="Not Covered",
            decision=Decision.CONFORMANT,
            evidence=available_evidence(),
        )


def test_record_preserves_traceability_fields() -> None:
    record = DecisionRecord(
        claim="KS-001",
        capability="Knowledge Lifecycle",
        executable_contract="contract.py",
        coverage_status="Covered",
        decision=Decision.CONFORMANT,
        evidence=available_evidence(),
    )

    assert record.claim == "KS-001"
    assert record.capability == "Knowledge Lifecycle"
    assert record.executable_contract == "contract.py"
    assert record.coverage_status == "Covered"
