from pathlib import Path


CHART = Path(
    "epics/epic077_veracity_transparency_sidecar/helm/veracity-transparency-sidecar"
)


def test_helm_chart_files_exist():

    assert (CHART / "Chart.yaml").exists()
    assert (CHART / "values.yaml").exists()
    assert (CHART / "templates/deployment.yaml").exists()


def test_chart_defines_sidecar_name():

    content = (CHART / "Chart.yaml").read_text()

    assert "veracity-transparency-sidecar" in content


def test_values_define_metrics_port():

    content = (CHART / "values.yaml").read_text()

    assert "metrics:" in content
    assert "port: 9090" in content


def test_deployment_defines_sidecar_container():

    content = (CHART / "templates/deployment.yaml").read_text()

    assert "veracity-transparency-sidecar" in content
    assert "VERACITY_TRANSPARENCY_BACKEND" in content
    assert "containerPort" in content
