from epics.ztc21_hardware_trust_anchors.hardware_trust_anchor import (
    HardwareTrustAnchor,
)


class HardwareAnchorVerifier:

    SUPPORTED_ANCHORS = {
        ("aws", "nitro_pcr"),
        ("gcp", "sev_snp"),
        ("azure", "azure_claim"),
        ("tpm", "tpm_quote"),
    }

    @classmethod
    def verify(
        cls,
        anchor: HardwareTrustAnchor,
    ) -> bool:

        if not anchor.measurement_hash:
            return False

        return (
            anchor.provider,
            anchor.anchor_type,
        ) in cls.SUPPORTED_ANCHORS
