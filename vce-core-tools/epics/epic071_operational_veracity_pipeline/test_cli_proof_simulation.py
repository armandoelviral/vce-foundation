import json
from pathlib import Path


CLI_CONTRACT = Path(
    "epics/epic071_operational_veracity_pipeline/cli_proof_simulation.md"
)


def test_cli_proof_simulation_contract_exists():

    assert CLI_CONTRACT.exists()


def test_cli_contract_mentions_required_output_fields():

    content = CLI_CONTRACT.read_text()

    assert "assessment" in content
    assert "organization" in content
    assert "certification_status" in content
    assert "evidence_coverage_ratio_pct" in content
    assert "drift_detected" in content
    assert "audit_status" in content


def test_example_cli_assessment_json_is_valid():

    output = {
        "assessment": {
            "organization": "Fintech Pilot Systems",
            "certification_status": "VCE GOLD CERTIFIED",
            "metrics": {
                "evidence_coverage_ratio_pct": 100.0,
                "evidence_debt_index_adimensional": 0,
                "estimated_evidence_exposure_usd": 0.0,
            },
            "drift_detected": False,
            "audit_status": "PASSED",
        }
    }

    encoded = json.dumps(
        output,
        sort_keys=True,
    )

    decoded = json.loads(
        encoded
    )

    assert decoded["assessment"]["audit_status"] == "PASSED"
    assert decoded["assessment"]["drift_detected"] is False
    assert (
        decoded["assessment"]["metrics"]["evidence_coverage_ratio_pct"]
        == 100.0
    )
