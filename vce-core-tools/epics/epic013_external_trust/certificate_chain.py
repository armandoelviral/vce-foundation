class CertificateChain:

    def verify(self, certificate):

        required_fields = [
            "issuer",
            "subject",
            "repository",
            "expires_at",
        ]

        for field in required_fields:
            if field not in certificate:
                return False

        if certificate["issuer"] != "github-actions":
            return False

        return True
