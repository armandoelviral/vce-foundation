import json
from io import StringIO
import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

import test_retail_report_jwt_composition as setup
import test_retail_vm_report_cli as cli_setup

from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action, GrantAdministrationRecord,
)
from sp001.infrastructure import retail_vm_report_cli as cli
from sp001.services.knowledge_source_integrity import digest_knowledge_source_content


@pytest.fixture(scope="module")
def keys():
    return tuple(
        rsa.generate_private_key(public_exponent=65537, key_size=2048)
        for _ in range(2)
    )


@pytest.mark.parametrize("during_read,expected_code", [
    ("unchanged", 0), ("revoked", 4), ("expired", 3),
    ("backend_failure", 6),
])
def test_reauthorizes_after_evidence_read_before_any_output(
    tmp_path, keys, monkeypatch, during_read, expected_code,
):
    path, service, grants, definitions = setup.environment(tmp_path, keys)
    credential = setup.token(keys[0])
    report = setup.make_report()
    service.save(
        credential=credential, identity=setup.IDENTITY, report=report,
    )
    (tmp_path / "evidence.bin").write_bytes(b"original")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "schema_version": 1,
        "evidence": [{
            "evidence_id": "EVIDENCE", "version": "1", "byte_length": 8,
            "sha256": digest_knowledge_source_content(content=b"original").value,
            "path": "evidence.bin",
        }],
    }), encoding="utf-8")
    args = cli_setup.arguments(path) + [
        "--evidence-manifest", str(manifest),
        "--max-manifest-bytes", "4096",
        "--max-evidence-bytes", "100",
    ]
    pem = keys[0].public_key().public_bytes(
        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")
    output, errors = StringIO(), StringIO()
    events = []
    real_compose = cli.compose_transactional_retail_reports
    real_compare = cli.compare_retail_evidence_manifest

    def compose(**kwargs):
        composed = real_compose(**kwargs)
        real_recover = composed.recover_with_admissions

        def recover(**arguments):
            events.append("authenticate_and_recover")
            if during_read == "backend_failure" and "evidence_read" in events:
                raise OSError("synthetic final recovery failure")
            return real_recover(**arguments)

        monkeypatch.setattr(composed, "recover_with_admissions", recover)
        return composed

    def compare(**kwargs):
        result = real_compare(**kwargs)
        assert output.getvalue() == ""
        events.append("evidence_read")
        if during_read == "revoked":
            for index, grant in enumerate(definitions):
                assert grants.apply(record=GrantAdministrationRecord(
                    f"FINAL-REVOKE-{index}", grant.principal,
                    Action.REVOKE, grant, int(time.time()),
                ))
        elif during_read == "expired":
            expiration = jwt.decode(
                credential, options={"verify_signature": False},
            )["exp"]
            monkeypatch.setattr(cli.time, "time", lambda: expiration)
        return result

    monkeypatch.setattr(cli, "compose_transactional_retail_reports", compose)
    monkeypatch.setattr(cli, "compare_retail_evidence_manifest", compare)

    code = cli.main(
        args, environment={"VM_TEST_PUBLIC_KEY": pem},
        stdin=StringIO(credential + "\n"), stdout=output, stderr=errors,
    )
    assert code == expected_code
    assert events == [
        "authenticate_and_recover", "evidence_read",
        "authenticate_and_recover",
    ]
    if expected_code == 0:
        assert "COINCIDENCIA DE BYTES" in output.getvalue()
        assert errors.getvalue() == ""
    else:
        assert output.getvalue() == ""
        assert errors.getvalue().strip()
        assert report.evaluations[0].rationale not in errors.getvalue()
    assert credential not in output.getvalue()
    assert credential not in errors.getvalue()
