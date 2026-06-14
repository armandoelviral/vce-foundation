from epics.ztc12_browser_verification_portal.browser_evidence_input import (
    BrowserEvidenceInput,
)


def test_browser_input_contains_raw_evidence():

    evidence = BrowserEvidenceInput(
        raw_json='{"artifact_id": "d5-001"}'
    )

    assert evidence.raw_json == '{"artifact_id": "d5-001"}'


def test_browser_input_serializes():

    evidence = BrowserEvidenceInput(
        raw_json='{"artifact_id": "d5-001"}'
    )

    assert evidence.to_dict() == {
        "raw_json": '{"artifact_id": "d5-001"}'
    }
