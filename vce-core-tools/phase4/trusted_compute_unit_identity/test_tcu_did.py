from phase4.trusted_compute_unit_identity.tcu_did import (
    TcuDid,
)


def test_contains_did():

    did = TcuDid(
        "did:tcn:gcp:us-central1:tcu-node-02"
    )

    assert did.value == (
        "did:tcn:gcp:us-central1:tcu-node-02"
    )


def test_serializes():

    did = TcuDid(
        "did:tcn:gcp:us-central1:tcu-node-02"
    )

    assert did.to_dict() == {
        "did":
        "did:tcn:gcp:us-central1:tcu-node-02"
    }


def test_rejects_empty():

    try:

        TcuDid("")

        assert False

    except ValueError:

        assert True
