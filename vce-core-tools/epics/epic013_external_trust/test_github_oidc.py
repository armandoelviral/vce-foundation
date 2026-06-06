from epics.epic013_external_trust.github_oidc import GitHubOIDCAdapter
from epics.epic013_external_trust.trust_boundary import TrustBoundary


def test_github_oidc_normalizes_claims():

    claims = {
        "iss": "github-actions",
        "sub": "repo:vce-foundation",
        "repository": "vce-foundation",
        "workflow": "ci.yml",
        "signature_valid": True,
    }

    adapter = GitHubOIDCAdapter()

    evidence = adapter.normalize(
        claims
    )

    assert evidence is not None


def test_github_oidc_evidence_passes_trust_boundary():

    claims = {
        "iss": "github-actions",
        "sub": "repo:vce-foundation",
        "repository": "vce-foundation",
        "workflow": "ci.yml",
        "signature_valid": True,
    }

    adapter = GitHubOIDCAdapter()

    evidence = adapter.normalize(
        claims
    )

    boundary = TrustBoundary(
        allowed_issuers=[
            "github-actions",
        ]
    )

    assert boundary.verify(
        evidence
    ) is True
