from has.runtime.specification_runtime import (
    Claim,
    ExecutionUnit,
)


def unit() -> ExecutionUnit:
    return ExecutionUnit(
        claim=Claim(
            identifier="CL-001",
            statement="Knowledge States exist.",
            contract="test_contract.py",
        ),
        contract="test_contract.py",
    )


def test_claim_is_preserved() -> None:
    assert (
        unit().claim.identifier
        == "CL-001"
    )


def test_contract_is_preserved() -> None:
    assert (
        unit().contract
        == "test_contract.py"
    )


def test_execution_returns_evidence() -> None:
    evidence, decision = unit().execute()

    assert evidence == (
        "Evidence for CL-001"
    )

    assert decision == "PASS"


def test_execution_unit_is_immutable() -> None:
    model = unit()

    try:
        model.contract = "other.py"
    except Exception:
        pass
    else:
        raise AssertionError(
            "ExecutionUnit shall be immutable."
        )


def test_execution_unit_equality() -> None:
    assert (
        unit()
        == unit()
    )
