from phase4.policy_adjudication_layer.dispute_resolution import (
    DisputeResolution,
)


def test_resolves_appeal():

    result = DisputeResolution.resolve(
        appeal_id="appeal-001",
        resolution="UPHELD",
    )

    assert result["appeal_id"] == "appeal-001"


def test_contains_resolution():

    result = DisputeResolution.resolve(
        appeal_id="appeal-001",
        resolution="UPHELD",
    )

    assert result["resolution"] == "UPHELD"


def test_serializes():

    result = DisputeResolution.resolve(
        appeal_id="appeal-001",
        resolution="UPHELD",
    )

    assert result == {
        "appeal_id": "appeal-001",
        "resolution": "UPHELD",
    }
