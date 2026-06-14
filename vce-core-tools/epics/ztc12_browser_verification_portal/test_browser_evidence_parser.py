from epics.ztc12_browser_verification_portal.browser_evidence_parser import (
    BrowserEvidenceParser,
)


def test_parses_valid_json():

    parsed = BrowserEvidenceParser.parse(
        '{"artifact_id":"d5-001"}'
    )

    assert parsed["artifact_id"] == "d5-001"


def test_rejects_invalid_json():

    try:
        BrowserEvidenceParser.parse(
            '{"artifact_id":'
        )
        assert False
    except ValueError:
        assert True
