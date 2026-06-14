from epics.ztc12_browser_verification_portal.evidence_schema_validator import (
    EvidenceSchemaValidator,
)


def test_accepts_valid_evidence():

    evidence = {
        "artifact_id": "d5-001",
        "schema_version": "v1",
        "state_root_hash": "root-001",
    }

    assert EvidenceSchemaValidator.validate(
        evidence
    )


def test_rejects_missing_artifact_id():

    evidence = {
        "schema_version": "v1",
        "state_root_hash": "root-001",
    }

    assert not EvidenceSchemaValidator.validate(
        evidence
    )


def test_rejects_missing_version():

    evidence = {
        "artifact_id": "d5-001",
        "state_root_hash": "root-001",
    }

    assert not EvidenceSchemaValidator.validate(
        evidence
    )


def test_rejects_missing_state_root():

    evidence = {
        "artifact_id": "d5-001",
        "schema_version": "v1",
    }

    assert not EvidenceSchemaValidator.validate(
        evidence
    )
