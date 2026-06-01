import hashlib
import json


class ReleaseArtifactAttestation:

    def create(
        self,
        artifact
    ):

        canonical = json.dumps(
            artifact,
            sort_keys=True,
            separators=(",", ":")
        )

        digest = hashlib.sha256(
            canonical.encode()
        ).hexdigest()


        return {
            "artifact": artifact,
            "digest": digest,
            "attestation_type": (
                "VCE_RELEASE_ARTIFACT"
            ),
            "verified": True
        }


    def verify(
        self,
        attestation
    ):

        artifact = attestation[
            "artifact"
        ]


        expected = hashlib.sha256(
            json.dumps(
                artifact,
                sort_keys=True,
                separators=(",", ":")
            ).encode()
        ).hexdigest()


        return (
            expected
            ==
            attestation["digest"]
        )
