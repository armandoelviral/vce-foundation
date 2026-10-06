import inspect
import json
from enum import StrEnum

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)


def test_decision_is_string_enum() -> None:
    assert issubclass(Decision, StrEnum)


def test_decision_has_exact_members() -> None:
    assert tuple(Decision) == (
        Decision.COMMIT,
        Decision.ABORT,
    )


def test_decision_has_exact_member_names() -> None:
    assert tuple(Decision.__members__) == (
        "COMMIT",
        "ABORT",
    )


@pytest.mark.parametrize(
    ("decision", "expected"),
    (
        (Decision.COMMIT, "COMMIT"),
        (Decision.ABORT, "ABORT"),
    ),
)
def test_decision_has_exact_value(
    decision: Decision,
    expected: str,
) -> None:
    assert decision.value == expected


@pytest.mark.parametrize(
    "decision",
    tuple(Decision),
)
def test_decision_is_nominal_string(
    decision: Decision,
) -> None:
    assert isinstance(decision, str)
    assert str(decision) == decision.value


@pytest.mark.parametrize(
    "decision",
    tuple(Decision),
)
def test_decision_round_trips_from_exact_value(
    decision: Decision,
) -> None:
    assert Decision(decision.value) is decision


@pytest.mark.parametrize(
    "value",
    (
        "",
        "commit",
        "abort",
        "COMMITTED",
        "ABORTED",
        "PREPARED",
        "COMMIT ",
        " ABORT",
    ),
)
def test_unknown_decision_value_is_rejected(
    value: str,
) -> None:
    with pytest.raises(ValueError):
        Decision(value)


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        0,
        1,
        True,
        False,
        b"COMMIT",
        (),
    ),
)
def test_non_string_value_is_rejected(
    value: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        Decision(value)


@pytest.mark.parametrize(
    "decision",
    tuple(Decision),
)
def test_decision_serializes_as_exact_json_string(
    decision: Decision,
) -> None:
    assert json.dumps(decision) == f'"{decision.value}"'


def test_decisions_are_distinct() -> None:
    assert Decision.COMMIT is not Decision.ABORT
    assert Decision.COMMIT != Decision.ABORT


def test_enum_defines_no_decision_derivation() -> None:
    source = inspect.getsource(Decision)

    assert "participant" not in source.lower()
    assert "preparation" not in source.lower()
    assert "verify" not in source.lower()
    assert "derive" not in source.lower()


def test_enum_defines_no_persistence_or_external_capability() -> None:
    source = inspect.getsource(Decision)

    for forbidden in (
        "sqlite",
        "database",
        "network",
        "http",
        "socket",
        "filesystem",
        "open(",
        "write(",
    ):
        assert forbidden not in source.lower()


def test_enum_defines_only_nominal_decisions() -> None:
    public_names = {
        name
        for name in Decision.__dict__
        if not name.startswith("_")
    }

    assert public_names == {
        "COMMIT",
        "ABORT",
    }
