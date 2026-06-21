import hashlib
import json


class TcuRegistryHasher:

    @staticmethod
    def hash_registry(
        registry,
    ) -> str:

        canonical = json.dumps(
            registry.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
        )

        return hashlib.sha256(
            canonical.encode("utf-8")
        ).hexdigest()
