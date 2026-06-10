from pathlib import Path


CONTRACT = Path(
    "epics/epic077_veracity_transparency_sidecar/prometheus_metrics_contract.md"
)


def test_prometheus_metrics_contract_exists():

    assert CONTRACT.exists()


def test_contract_lists_required_metrics():

    content = CONTRACT.read_text()

    assert "veracity_anchor_jobs_total" in content
    assert "veracity_anchor_success_total" in content
    assert "veracity_anchor_failure_total" in content
    assert "veracity_anchor_retry_total" in content
    assert "veracity_pending_jobs" in content
    assert "veracity_anchor_latency_seconds" in content
    assert "veracity_rekor_set_total" in content


def test_contract_defines_metric_types():

    content = CONTRACT.read_text()

    assert "counter" in content
    assert "gauge" in content
    assert "histogram" in content


def test_contract_defines_required_labels():

    content = CONTRACT.read_text()

    assert "backend" in content
    assert "status" in content
    assert "namespace" in content
    assert "pod" in content
    assert "error_code" in content


def test_contract_requires_low_cardinality():

    content = CONTRACT.read_text()

    assert "low cardinality" in content
    assert "scrapeable by Prometheus" in content
    assert "suitable for Grafana dashboards" in content
