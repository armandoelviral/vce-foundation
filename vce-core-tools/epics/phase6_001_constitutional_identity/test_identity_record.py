from epics.phase6_001_constitutional_identity.identity_record import (
    IdentityRecord,
)


def test_identity_record_creation():
    record = IdentityRecord(
        identity_id="identity.001",
        subject_id="subject.001",
        identity_type="human",
    )

    assert record.identity_id == "identity.001"


def test_rejects_empty_identity_id():
    try:
        IdentityRecord(
            "",
            "subject.001",
            "human",
        )
        assert False
    except ValueError as exc:
        assert "identity_id" in str(exc)


def test_rejects_empty_subject():
    try:
        IdentityRecord(
            "identity.001",
            "",
            "human",
        )
        assert False
    except ValueError as exc:
        assert "subject_id" in str(exc)
