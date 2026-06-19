from phase3.authority_governance.authority_record import (
    AuthorityRecord,
)


def test_record_contains_id():

    authority = AuthorityRecord(
        authority_id="auth-001",
        principal_id="principal-001",
        role="GOVERNOR",
    )

    assert authority.authority_id == "auth-001"


def test_record_contains_principal():

    authority = AuthorityRecord(
        authority_id="auth-001",
        principal_id="principal-001",
        role="GOVERNOR",
    )

    assert authority.principal_id == "principal-001"


def test_record_contains_role():

    authority = AuthorityRecord(
        authority_id="auth-001",
        principal_id="principal-001",
        role="GOVERNOR",
    )

    assert authority.role == "GOVERNOR"


def test_record_serializes():

    authority = AuthorityRecord(
        authority_id="auth-001",
        principal_id="principal-001",
        role="GOVERNOR",
    )

    assert authority.to_dict() == {
        "authority_id": "auth-001",
        "principal_id": "principal-001",
        "role": "GOVERNOR",
    }
