import hashlib
import json
import time


class SLSAGenerator:

    def generate(
        self,
        source,
        artifact
    ):

        statement = {
            "_type":
                "https://in-toto.io/Statement/v1",

            "predicateType":
                "https://slsa.dev/provenance/v1",

            "subject": artifact,

            "predicate": {
                "builder": {
                    "id":
                        "vce-runtime-builder"
                },

                "buildType":
                    "vce.secure.runtime",

                "source":
                    source,

                "timestamp":
                    int(
                        time.time()
                    )
            }
        }


        canonical = json.dumps(
            statement,
            sort_keys=True,
            separators=(",", ":")
        )


        digest = hashlib.sha256(
            canonical.encode()
        ).hexdigest()


        return {
            "statement": statement,
            "digest": digest,
            "verified": True
        }
