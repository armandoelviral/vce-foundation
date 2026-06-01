import json
import base64

from epics.epic017_supply_chain.github_oidc_verifier import (
    GitHubOIDCVerifier
)


def encode(data):

    raw = json.dumps(
        data
    ).encode()

    return (
        base64.urlsafe_b64encode(
            raw
        )
        .decode()
        .rstrip("=")
    )


payload = encode(
    {
        "iss":
            "https://token.actions.githubusercontent.com",

        "repository":
            "vce-foundation/vce-core-tools",

        "sub":
            "repo:vce-foundation/vce-core-tools"
    }
)


fake_jwt = (
    "header."
    +
    payload
    +
    ".signature"
)


verifier = GitHubOIDCVerifier()


result = verifier.verify(
    fake_jwt
)


print(
    result["valid_issuer"]
)


print(
    result["repository"]
)
