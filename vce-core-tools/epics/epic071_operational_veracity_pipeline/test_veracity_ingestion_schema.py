from pathlib import Path


SCHEMA = Path(
    "epics/epic071_operational_veracity_pipeline/veracity_ingestion_schema.md"
)


def test_ingestion_schema_exists():

    assert SCHEMA.exists()


def test_schema_defines_six_layers():

    content = SCHEMA.read_text()

    assert "Identity Layer" in content
    assert "Trust Layer" in content
    assert "Provenance Layer" in content
    assert "Replay Layer" in content
    assert "Evidence Layer" in content
    assert "Governance Layer" in content


def test_schema_defines_provenance_fields():

    content = SCHEMA.read_text()

    assert "input_hash" in content
    assert "code_hash" in content
    assert "environment_hash" in content
    assert "dependency_hash" in content


def test_schema_defines_replay_fields():

    content = SCHEMA.read_text()

    assert "replay_uri" in content
    assert "deterministic_checksum" in content
    assert "runtime_version" in content
    assert "sequence_number" in content


def test_schema_requires_validation_before_anchoring():

    content = SCHEMA.read_text()

    assert "schema validation" in content
    assert "hash validation" in content
    assert "required field validation" in content
    assert "replay metadata validation" in content
