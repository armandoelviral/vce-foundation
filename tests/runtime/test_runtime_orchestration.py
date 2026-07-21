from has.runtime.specification_runtime import (
    Claim,
    ExecutionResult,
    Specification,
    SpecificationRuntime,
)


def specification() -> Specification:
    return Specification(
        identifier="SPEC-001",
        claims=(
            Claim(
                identifier="CL-001",
                statement="Claim One",
                contract="contract_one.py",
            ),
            Claim(
                identifier="CL-002",
                statement="Claim Two",
                contract="contract_two.py",
            ),
        ),
    )


def runtime() -> SpecificationRuntime:
    return SpecificationRuntime()


def test_runtime_executes_every_claim() -> None:
    result = runtime().execute(
        specification()
    )

    assert len(
        result.evidence
    ) == 2


def test_runtime_preserves_specification_identifier() -> None:
    result = runtime().execute(
        specification()
    )

    assert (
        result.specification_identifier
        == "SPEC-001"
    )


def test_runtime_returns_execution_result() -> None:
    result = runtime().execute(
        specification()
    )

    assert isinstance(
        result,
        ExecutionResult,
    )


def test_runtime_returns_pass() -> None:
    result = runtime().execute(
        specification()
    )

    assert result.passed is True

    assert result.decision == "PASS"


def test_runtime_is_deterministic() -> None:
    first = runtime().execute(
        specification()
    )

    second = runtime().execute(
        specification()
    )

    assert first == second


def test_every_claim_produces_evidence() -> None:
    result = runtime().execute(
        specification()
    )

    assert all(
        evidence
        for evidence in result.evidence
    )
