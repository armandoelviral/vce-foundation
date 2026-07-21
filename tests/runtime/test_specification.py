from has.runtime.specification_runtime import (
    Claim,
    Specification,
)


def specification() -> Specification:
    return Specification(
        identifier="SPEC-001",
        claims=(
            Claim(
                identifier="CL-001",
                statement="Knowledge States exist.",
                contract="test_contract.py",
            ),
        ),
    )


def test_identifier_is_preserved() -> None:
    assert (
        specification().identifier
        == "SPEC-001"
    )


def test_claims_are_preserved() -> None:
    assert len(
        specification().claims
    ) == 1


def test_specification_is_immutable() -> None:
    spec = specification()

    try:
        spec.identifier = "OTHER"
    except Exception:
        pass
    else:
        raise AssertionError(
            "Specification shall be immutable."
        )


def test_specification_equality() -> None:
    assert (
        specification()
        == specification()
    )
