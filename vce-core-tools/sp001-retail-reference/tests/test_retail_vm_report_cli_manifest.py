import json
from io import StringIO
import os
from pathlib import Path
import subprocess
import sys

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

import test_retail_report_jwt_composition as setup
import test_retail_vm_report_cli as cli_setup

from sp001.infrastructure import retail_vm_report_cli as cli
from sp001.infrastructure import retail_evidence_manifest as manifest_module
from sp001.services.knowledge_source_integrity import digest_knowledge_source_content


@pytest.fixture(scope="module")
def keys():
    return tuple(
        rsa.generate_private_key(public_exponent=65537, key_size=2048)
        for _ in range(2)
    )


def prepare(tmp_path, keys):
    path, service, _, _ = setup.environment(tmp_path, keys)
    credential = setup.token(keys[0])
    service.save(
        credential=credential, identity=setup.IDENTITY, report=setup.make_report(),
    )
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "schema_version": 1,
        "evidence": [{
            "evidence_id": "EVIDENCE", "version": "1", "byte_length": 8,
            "sha256": digest_knowledge_source_content(content=b"original").value,
            "path": "evidence.bin",
        }],
    }), encoding="utf-8")
    pem = keys[0].public_key().public_bytes(
        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")
    args = cli_setup.arguments(path) + [
        "--evidence-manifest", str(manifest),
        "--max-manifest-bytes", "4096",
        "--max-evidence-bytes", "100",
    ]
    return credential, manifest, pem, args


def invoke(args, credential, pem):
    output, errors = StringIO(), StringIO()
    code = cli.main(
        args, environment={"VM_TEST_PUBLIC_KEY": pem},
        stdin=StringIO(credential + "\n"), stdout=output, stderr=errors,
    )
    return code, output.getvalue(), errors.getvalue()


@pytest.mark.parametrize("scenario,label", [
    ("match", "COINCIDENCIA DE BYTES"),
    ("different", "CONTENIDO DIFERENTE"),
    ("missing", "ARCHIVO NO ENCONTRADO"),
    ("undeclared", "SIN EXPECTATIVA DECLARADA"),
])
def test_cli_presents_manifest_comparisons(tmp_path, keys, scenario, label):
    credential, manifest, pem, args = prepare(tmp_path, keys)
    if scenario == "match":
        (tmp_path / "evidence.bin").write_bytes(b"original")
    elif scenario == "different":
        (tmp_path / "evidence.bin").write_bytes(b"modified")
    elif scenario == "undeclared":
        manifest.write_text(
            '{"schema_version":1,"evidence":[]}', encoding="utf-8",
        )
    code, output, errors = invoke(args, credential, pem)
    assert code == 0, errors
    assert errors == ""
    assert label in output
    assert "Synthetic rationale." in output
    assert credential not in output


def test_denied_recovery_never_reads_manifest(tmp_path, keys, monkeypatch):
    _, manifest, pem, args = prepare(tmp_path, keys)
    manifest.unlink()

    def forbidden(**kwargs):
        raise AssertionError("manifest must not be read before authorization")

    monkeypatch.setattr(cli, "compare_retail_evidence_manifest", forbidden)
    code, output, _ = invoke(args, setup.token(keys[1]), pem)
    assert code == 3
    assert output == ""


@pytest.mark.parametrize("fault", ["duplicate_key", "foreign", "oversized"])
def test_invalid_manifest_exports_no_report(tmp_path, keys, fault, monkeypatch):
    credential, manifest, pem, args = prepare(tmp_path, keys)
    if fault == "duplicate_key":
        manifest.write_text(
            '{"schema_version":1,"schema_version":1,"evidence":[]}',
            encoding="utf-8",
        )
    elif fault == "foreign":
        document = json.loads(manifest.read_text())
        document["evidence"][0]["evidence_id"] = "OTHER"
        manifest.write_text(json.dumps(document), encoding="utf-8")
    else:
        manifest.write_bytes(b" " * 4097)

    calls = []
    def forbidden(**kwargs):
        calls.append(True)
        raise AssertionError("invalid manifest must not open evidence")

    monkeypatch.setattr(manifest_module, "compare_evidence_file", forbidden)
    code, output, errors = invoke(args, credential, pem)
    assert code == 6
    assert output == ""
    assert calls == []
    assert credential not in errors


def test_cli_manifest_flow_runs_as_separate_process(tmp_path, keys):
    credential, _, pem, args = prepare(tmp_path, keys)
    (tmp_path / "evidence.bin").write_bytes(b"original")
    root = Path(__file__).resolve().parents[1]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(root / "src")
    environment["VM_TEST_PUBLIC_KEY"] = pem
    completed = subprocess.run(
        [sys.executable, "-m", "sp001.infrastructure.retail_vm_report_cli", *args],
        input=credential + "\n", capture_output=True, text=True,
        encoding="utf-8", cwd=root, env=environment, timeout=30,
    )
    assert completed.returncode == 0, completed.stderr
    assert "COINCIDENCIA DE BYTES" in completed.stdout
    assert completed.stderr == ""
    assert credential not in completed.stdout
