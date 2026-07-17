from has.conformance.model.decision import (
    Decision,
)


def test_conformant_value() -> None:
    assert (
        Decision.CONFORMANT.value
        == "Conformant"
    )


def test_non_conformant_value() -> None:
    assert (
        Decision.NON_CONFORMANT.value
        == "Non-Conformant"
    )


def test_conformant_property() -> None:
    assert Decision.CONFORMANT.is_conformant

    assert not Decision.CONFORMANT.is_non_conformant


def test_non_conformant_property() -> None:
    assert Decision.NON_CONFORMANT.is_non_conformant

    assert not Decision.NON_CONFORMANT.is_conformant


def test_two_decisions_exist() -> None:
    assert len(list(Decision)) == 2
