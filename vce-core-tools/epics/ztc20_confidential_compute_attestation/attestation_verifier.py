from epics.ztc20_confidential_compute_attestation.attestation_evidence import (
    AttestationEvidence,
)


class AttestationVerifier:

    SUPPORTED_PROVIDERS = {
        "aws",
        "gcp",
        "azure",
    }

    @classmethod
    def verify(
        cls,
        evidence: AttestationEvidence,
    ) -> bool:

        if not evidence.witness_id:
            return False

        if evidence.provider not in cls.SUPPORTED_PROVIDERS:
            return False

        if not evidence.evidence_hash:
            return False

        return True
