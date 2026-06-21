from phase4.trusted_compute_unit_identity.tcu_identity_block import (
    TcuIdentityBlock,
)

from phase4.trusted_compute_unit_identity.tcu_identity_hasher import (
    TcuIdentityHasher,
)

from phase4.trusted_compute_unit_identity.tcu_identity_signatures import (
    TcuIdentitySignatures,
)

from phase4.trusted_compute_unit_identity.tcu_attestation_binding import (
    TcuAttestationBinding,
)


class TcuIdentityFlow:

    @staticmethod
    def generate():

        identity = TcuIdentityBlock(
            did="did:tcn:gcp:us-central1:tcu-node-02",
            ed25519_public_key="ed25519-pub-001",
            mldsa65_public_key="mldsa65-pub-001",
        )

        identity_hash = (
            TcuIdentityHasher.hash_identity(
                identity
            )
        )

        signatures = (
            TcuIdentitySignatures(
                ed25519_signature="ed25519-sig-001",
                mldsa65_signature="mldsa65-sig-001",
            )
        )

        binding = (
            TcuAttestationBinding(
                identity_hash=identity_hash,
                attestation_root="attestation-root-001",
            )
        )

        return {
            "identity":
                identity.to_dict(),
            "identity_hash":
                identity_hash,
            "signatures":
                signatures.to_dict(),
            "attestation_binding":
                binding.to_dict(),
        }
