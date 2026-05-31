from github_oidc import GitHubOIDCAdapter
from trust_boundary import TrustBoundary


claims = {
    "iss": "github-actions",
    "sub": "repo:vce-foundation",
    "repository": "vce-foundation",
    "workflow": "ci.yml",
    "signature_valid": True
}


adapter = GitHubOIDCAdapter()

evidence = adapter.normalize(
    claims
)


boundary = TrustBoundary(
    [
        "github-actions"
    ]
)


print(evidence)

print(
    boundary.verify(
        evidence
    )
)
