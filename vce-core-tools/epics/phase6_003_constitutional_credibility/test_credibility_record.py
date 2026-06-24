from epics.phase6_003_constitutional_credibility.credibility_record import (
    CredibilityRecord,
)


def test_credibility_record_creation():
    record = CredibilityRecord(
        credibility_id="cred.001",
        identity_id="identity.001",
        credibility_delta=10,
    )

    assert record.credibility_id == "cred.001"


def test_requires_credibility_id():
    try:
        CredibilityRecord(
            "",
            "identity.001",
            10,
        )
        assert False
    except ValueError as exc:
        assert "credibility_id" in str(exc)
