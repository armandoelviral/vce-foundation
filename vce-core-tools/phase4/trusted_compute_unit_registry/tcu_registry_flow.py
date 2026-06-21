from phase4.trusted_compute_unit_registry.tcu_registry import (
    TcuRegistry,
)

from phase4.trusted_compute_unit_registry.tcu_registry_entry import (
    TcuRegistryEntry,
)

from phase4.trusted_compute_unit_registry.tcu_registry_hasher import (
    TcuRegistryHasher,
)

from phase4.trusted_compute_unit_registry.tcu_registry_verifier import (
    TcuRegistryVerifier,
)


class TcuRegistryFlow:

    @staticmethod
    def generate():

        registry = TcuRegistry()

        registry.add(
            TcuRegistryEntry(
                did="did:tcn:test:01",
                identity_hash="identity-001",
                attestation_root="attestation-001",
                status="ACTIVE",
            )
        )

        registry_hash = (
            TcuRegistryHasher.hash_registry(
                registry
            )
        )

        verified = (
            TcuRegistryVerifier.verify(
                registry,
                "did:tcn:test:01",
            )
        )

        return {
            "entries":
                registry.to_dict()["entries"],
            "registry_hash":
                registry_hash,
            "member_verified":
                verified,
        }
