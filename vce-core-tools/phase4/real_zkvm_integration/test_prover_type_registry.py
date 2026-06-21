from phase4.real_zkvm_integration.prover_type_registry import (
    ProverTypeRegistry,
)


def test_registry_starts_empty():

    registry = ProverTypeRegistry()

    assert registry.count() == 0


def test_register_sp1():

    registry = ProverTypeRegistry()

    registry.register(
        "SP1"
    )

    assert registry.count() == 1


def test_register_risc_zero():

    registry = ProverTypeRegistry()

    registry.register(
        "RISC_ZERO"
    )

    assert registry.count() == 1


def test_lists_registered_provers():

    registry = ProverTypeRegistry()

    registry.register("SP1")
    registry.register("RISC_ZERO")

    assert registry.prover_types() == [
        "SP1",
        "RISC_ZERO",
    ]


def test_contains_registered_prover():

    registry = ProverTypeRegistry()

    registry.register("SP1")

    assert registry.contains(
        "SP1"
    ) is True
