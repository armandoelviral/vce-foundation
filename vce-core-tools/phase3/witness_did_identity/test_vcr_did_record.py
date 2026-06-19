from phase3.witness_did_identity.vcr_did_record import (
    VcrDidRecord,
)


def test_contains_did():

    record = VcrDidRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
    )

    assert (
        record.did
        == "did:vcr:gcp:us-central1:fp001"
    )


def test_contains_controller():

    record = VcrDidRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
    )

    assert (
        record.controller
        == "did:vcr:authority:main"
    )


def test_is_vcr_method():

    record = VcrDidRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
    )

    assert (
        record.did.startswith(
            "did:vcr:"
        )
    )


def test_serializes():

    record = VcrDidRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
    )

    assert record.to_dict() == {
        "did":
            "did:vcr:gcp:us-central1:fp001",

        "controller":
            "did:vcr:authority:main",
    }
