import hashlib
import json


class ReproducibleBuildProof:

    def build_hash(
        self,
        source_manifest
    ):

        canonical = json.dumps(
            source_manifest,
            sort_keys=True,
            separators=(",", ":")
        )

        return hashlib.sha256(
            canonical.encode()
        ).hexdigest()


    def verify(
        self,
        first_build,
        second_build
    ):

        return (
            first_build
            ==
            second_build
        )
