from epics.epic013_external_trust.certificate_chain import CertificateChain
from epics.epic013_external_trust.transparency_log import TransparencyLog
from epics.epic013_external_trust.trust_boundary import TrustBoundary

class ExternalTrustEngine:

    def __init__(self):

        self.cert_chain = CertificateChain()
        self.log = TransparencyLog()

        self.boundary = TrustBoundary(
            [
                "github-actions"
            ]
        )


    def verify(self, certificate, artifact):

        if not self.cert_chain.verify(
            certificate
        ):
            return False

        entry = self.log.create_entry(
            artifact
        )

        if not self.log.verify_inclusion(
            entry
        ):
            return False


        evidence = {
            "issuer": certificate[
                "issuer"
            ],
            "signature_valid": True
        }


        return self.boundary.verify(
            evidence
        )
