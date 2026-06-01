class FulcioVerifier:

    TRUSTED_ISSUER = (
        "https://fulcio.sigstore.dev"
    )


    def verify(
        self,
        certificate
    ):

        issuer_valid = (
            certificate.get(
                "issuer"
            )
            ==
            self.TRUSTED_ISSUER
        )


        identity_present = all(
            [
                certificate.get(
                    "subject"
                ),

                certificate.get(
                    "repository"
                ),

                certificate.get(
                    "workflow"
                )
            ]
        )


        return {
            "issuer_valid": issuer_valid,
            "identity_valid": identity_present,
            "certificate_valid": (
                issuer_valid
                and
                identity_present
            )
        }
