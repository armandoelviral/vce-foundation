from phase4.trusted_compute_unit_identity.tcu_identity_flow import (
    TcuIdentityFlow,
)


def test_generates_complete_identity():

    result = TcuIdentityFlow.generate()

    assert "identity" in result
    assert "identity_hash" in result
    assert "signatures" in result
    assert "attestation_binding" in result


def test_identity_hash_present():

    result = TcuIdentityFlow.generate()

    assert len(
        result["identity_hash"]
    ) == 64
