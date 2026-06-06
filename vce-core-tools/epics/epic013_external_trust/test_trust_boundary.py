from epics.epic013_external_trust.trust_boundary import TrustBoundary


def test_trust_boundary_accepts_allowed_issuer():

    boundary = TrustBoundary(
        allowed_issuers=[
            "github-actions",
        ]
    )

    artifact = {
        "issuer": "github-actions",
        "signature_valid": True,
    }

    assert boundary.verify(artifact) is True


def test_trust_boundary_rejects_unknown_issuer():

    boundary = TrustBoundary(
        allowed_issuers=[
            "github-actions",
        ]
    )

    artifact = {
        "issuer": "unknown-runner",
        "signature_valid": True,
    }

    assert boundary.verify(artifact) is False


def test_trust_boundary_rejects_invalid_signature():

    boundary = TrustBoundary(
        allowed_issuers=[
            "github-actions",
        ]
    )

    artifact = {
        "issuer": "github-actions",
        "signature_valid": False,
    }

    assert boundary.verify(artifact) is False
