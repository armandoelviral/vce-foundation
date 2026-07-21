from has.runtime.specification_runtime import (
    ExecutionResult,
)


def result() -> ExecutionResult:
    return ExecutionResult(
        specification_identifier="SPEC-001",
        passed=True,
        evidence=(
            "CL-001",
            "CL-002",
        ),
        decision="PASS",
    )


def test_specification_identifier_is_preserved() -> None:
    assert (
        result().specification_identifier
        == "SPEC-001"
    )


def test_passed_state_is_preserved() -> None:
    assert result().passed is True


def test_evidence_is_preserved() -> None:
    assert result().evidence == (
        "CL-001",
        "CL-002",
    )


def test_decision_is_preserved() -> None:
    assert (
        result().decision
        == "PASS"
    )


def test_execution_result_is_immutable() -> None:
    model = result()

    try:
        model.decision = "FAIL"
    except Exception:
        pass
    else:
        raise AssertionError(
            "ExecutionResult shall be immutable."
        )


def test_execution_result_equality() -> None:
    assert (
        result()
        == result()
    )
