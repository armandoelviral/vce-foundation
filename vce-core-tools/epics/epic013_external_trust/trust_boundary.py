class TrustBoundary:

    def __init__(self, allowed_issuers):
        self.allowed_issuers = allowed_issuers

    def verify(self, evidence):
        issuer = evidence.get("issuer")
        signature_valid = evidence.get("signature_valid", False)

        if issuer not in self.allowed_issuers:
            return False

        if not signature_valid:
            return False

        return True
