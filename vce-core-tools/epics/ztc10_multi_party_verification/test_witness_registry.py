from epics.ztc10_multi_party_verification.witness_contract import (
    WitnessContract,
)

from epics.ztc10_multi_party_verification.witness_registry import (
    WitnessRegistry,
)


def test_registry_registers_witness():

    registry = WitnessRegistry()

    witness = WitnessContract(
        witness_id="witness-001",
        public_key="public-key-001",
    )

    registry.register(witness)

    assert registry.exists("witness-001")


def test_registry_rejects_unknown_witness():

    registry = WitnessRegistry()

    assert not registry.exists("missing-witness")
