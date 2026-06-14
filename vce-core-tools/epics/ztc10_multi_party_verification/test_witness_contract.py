from epics.ztc10_multi_party_verification.witness_contract import (
    WitnessContract,
)


def test_witness_contract_contains_identity():

    witness = WitnessContract(
        witness_id="witness-001",
        public_key="public-key",
    )

    assert witness.witness_id == "witness-001"
    assert witness.public_key == "public-key"


def test_witness_contract_serializes():

    witness = WitnessContract(
        witness_id="witness-001",
        public_key="public-key",
    )

    assert witness.to_dict() == {
        "witness_id": "witness-001",
        "public_key": "public-key",
    }
