#!/usr/bin/env python3

class FulcioValidator:

    def verify_ephemeral_certificate(
        self,
        certificate_pem: str,
        expected_identity: str
    ) -> bool:

        if not certificate_pem:
            return False

        if "BEGIN CERTIFICATE" not in certificate_pem:
            return False

        if expected_identity not in certificate_pem:
            return False

        return True
