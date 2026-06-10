from pathlib import Path


CONTRACT = Path(
    "epics/epic077_veracity_transparency_sidecar/sidecar_iam_boundary_policy.md"
)


def test_iam_boundary_contract_exists():

    assert CONTRACT.exists()


def test_contract_defines_core_principle():

    content = CONTRACT.read_text()

    assert "least-privilege" in content
    assert "sign proofs" in content
    assert "write evidence" in content


def test_contract_denies_sensitive_data_access():

    content = CONTRACT.read_text()

    assert "access PHI" in content
    assert "access PII" in content
    assert "access biometrics" in content
    assert "access application databases" in content


def test_contract_defines_kms_boundaries():

    content = CONTRACT.read_text()

    assert "kms:Sign" in content
    assert "kms:Verify" in content

    assert "kms:CreateKey" in content
    assert "kms:ScheduleKeyDeletion" in content


def test_contract_defines_s3_boundaries():

    content = CONTRACT.read_text()

    assert "s3:PutObject" in content
    assert "s3:GetObject" in content

    assert "s3:DeleteObject" in content
    assert "s3:DeleteObjectVersion" in content


def test_contract_requires_dedicated_service_account():

    content = CONTRACT.read_text()

    assert "dedicated ServiceAccount" in content
    assert "customer-facing services" in content


def test_contract_requires_pod_identity_constraints():

    content = CONTRACT.read_text()

    assert "pods.eks.amazonaws.com" in content
    assert "approved namespace" in content
    assert "approved service account" in content
