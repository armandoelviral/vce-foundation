from has.runtime.specification_runtime import (
    Claim,
    Specification,
    SpecificationRuntime,
)


def specification() -> Specification:
    return Specification(
        identifier="SPEC-001",
        claims=(
            Claim(
                identifier="CL-001",
                statement="Knowledge States exist.",
                contract="contract_a.py",
            ),
            Claim(
                identifier="CL-002",
                statement="Replay is deterministic.",
                contract="contract_b.py",
            ),
        ),
    )


def test_specification_executes() -> None:
    runtime = SpecificationRuntime()

    result = runtime.execute(
        specification()
    )

    assert result.passed is True

    assert result.decision == "PASS"

    assert result.specification_identifier == "SPEC-001"

    assert len(
        result.evidence
    ) == 2


def test_execution_is_deterministic() -> None:
    runtime = SpecificationRuntime()

    first = runtime.execute(
        specification()
    )

    second = runtime.execute(
        specification()
    )

    assert first == second

