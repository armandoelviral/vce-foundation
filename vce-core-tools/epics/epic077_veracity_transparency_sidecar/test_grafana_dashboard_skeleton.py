import json

from pathlib import Path


DASHBOARD = Path(
    "epics/epic077_veracity_transparency_sidecar/grafana/dashboard.json"
)


def test_dashboard_exists():

    assert DASHBOARD.exists()


def test_dashboard_is_valid_json():

    payload = json.loads(
        DASHBOARD.read_text()
    )

    assert payload["title"] == (
        "Veracity Transparency Sidecar"
    )


def test_dashboard_contains_required_panels():

    payload = json.loads(
        DASHBOARD.read_text()
    )

    panel_titles = {
        panel["title"]
        for panel in payload["panels"]
    }

    assert "Anchor Jobs Total" in panel_titles
    assert "Anchor Success Total" in panel_titles
    assert "Anchor Failure Total" in panel_titles
    assert "Pending Jobs" in panel_titles
    assert "Anchor Latency" in panel_titles


def test_dashboard_uses_veracity_metrics():

    content = DASHBOARD.read_text()

    assert "veracity_anchor_jobs_total" in content
    assert "veracity_anchor_success_total" in content
    assert "veracity_anchor_failure_total" in content
    assert "veracity_pending_jobs" in content
    assert "veracity_anchor_latency_seconds" in content
