class GitHubOIDCAdapter:

    def normalize(self, oidc_claims):

        return {
            "issuer": oidc_claims.get(
                "iss"
            ),

            "subject": oidc_claims.get(
                "sub"
            ),

            "repository": oidc_claims.get(
                "repository"
            ),

            "workflow": oidc_claims.get(
                "workflow"
            ),

            "signature_valid": oidc_claims.get(
                "signature_valid",
                False
            )
        }
