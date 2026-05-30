from rekor_validator import RekorValidator
from fulcio_validator import FulcioValidator


class Epic010Pipeline:

    def __init__(self):

        self.rekor = RekorValidator()
        self.fulcio = FulcioValidator()

    def validate(
        self,
        certificate_pem,
        expected_identity,
        rekor_entry
    ):

        if not self.fulcio.verify_ephemeral_certificate(
            certificate_pem,
            expected_identity
        ):
            return "REJECTED_FULCIO"

        if not self.rekor.verify_inclusion_proof(
            rekor_entry
        ):
            return "REJECTED_REKOR"

        return "ACCEPTED"
