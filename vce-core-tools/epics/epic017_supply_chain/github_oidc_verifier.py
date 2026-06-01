import json
import base64


class GitHubOIDCVerifier:

    TRUSTED_ISSUER = (
        "https://token.actions.githubusercontent.com"
    )


    def decode_payload(
        self,
        token
    ):

        parts = token.split(".")

        if len(parts) != 3:
            raise ValueError(
                "INVALID_JWT_FORMAT"
            )


        payload = parts[1]

        padding = (
            "=" * (-len(payload) % 4)
        )


        decoded = base64.urlsafe_b64decode(
            payload + padding
        )


        return json.loads(
            decoded
        )


    def verify(
        self,
        token
    ):

        claims = self.decode_payload(
            token
        )


        return {
            "valid_issuer":
                claims.get("iss")
                ==
                self.TRUSTED_ISSUER,

            "repository":
                claims.get(
                    "repository"
                ),

            "subject":
                claims.get(
                    "sub"
                )
        }
