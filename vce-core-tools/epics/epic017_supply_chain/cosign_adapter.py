from epics.epic017_supply_chain.fulcio_verifier import (
    FulcioVerifier
)

from epics.epic017_supply_chain.rekor_client import (
    RekorClient
)


class CosignAdapter:

    def __init__(self):

        self.fulcio = FulcioVerifier()
        self.rekor = RekorClient()


    def verify(
        self,
        artifact,
        certificate
    ):

        cert_result = (
            self.fulcio.verify(
                certificate
            )
        )


        if not cert_result[
            "certificate_valid"
        ]:

            return {
                "verified": False,
                "reason": "CERTIFICATE_FAILED"
            }


        entry = (
            self.rekor.create_entry(
                artifact
            )
        )


        rekor_valid = (
            self.rekor.verify_entry(
                entry
            )
        )


        return {
            "verified": rekor_valid,
            "certificate": True,
            "rekor": rekor_valid
        }

