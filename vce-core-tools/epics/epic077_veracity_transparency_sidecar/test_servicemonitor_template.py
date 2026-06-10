from pathlib import Path


TEMPLATE = Path(
    "epics/epic077_veracity_transparency_sidecar/helm/veracity-transparency-sidecar/templates/servicemonitor.yaml"
)


def test_servicemonitor_template_exists():

    assert TEMPLATE.exists()


def test_servicemonitor_defines_kind():

    content = TEMPLATE.read_text()

    assert "kind: ServiceMonitor" in content
    assert "monitoring.coreos.com/v1" in content


def test_servicemonitor_uses_metrics_port():

    content = TEMPLATE.read_text()

    assert "port: metrics" in content
    assert "path: /metrics" in content
    assert "interval: 30s" in content


def test_servicemonitor_is_metrics_gated():

    content = TEMPLATE.read_text()

    assert "{{- if .Values.metrics.enabled }}" in content
