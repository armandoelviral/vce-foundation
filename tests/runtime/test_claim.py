from has.runtime.specification_runtime import (
    Claim,
)


def claim() -> Claim:
    return Claim(
        identifier="CL-001",
        statement="Knowledge States exist.",
        contract="test_contract.py",
    )


def test_identifier_is_preserved() -> None:
    assert (
        claim().identifier
        == "CL-001"
    )


def test_statement_is_preserved() -> None:
    assert (
        claim().statement
        == "Knowledge States exist."
    )


def test_contract_reference_is_preserved() -> None:
    assert (
        claim().contract
        == "test_contract.py"
    )


def test_claim_is_immutable() -> None:
    model = claim()

    try:
        model.statement = "Modified"
    except Exception:
        pass
    else:
        raise AssertionError(
            "Claim shall be immutable."
        )


def test_claim_equality() -> None:
    assert (
        claim()
        == claim()
    )
