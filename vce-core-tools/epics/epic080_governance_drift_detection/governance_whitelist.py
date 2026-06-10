class GovernanceWhitelist:

    def __init__(
        self,
        manifests,
    ):

        self._manifests = manifests

    def is_approved(
        self,
        fingerprint,
    ):

        for manifest in self._manifests:

            if (
                manifest.model_id == fingerprint.model_id
                and manifest.model_version == fingerprint.model_version
                and manifest.model_hash == fingerprint.model_hash
                and manifest.weights_hash == fingerprint.weights_hash
                and manifest.runtime_image_hash
                == fingerprint.runtime_image_hash
            ):
                return True

        return False
