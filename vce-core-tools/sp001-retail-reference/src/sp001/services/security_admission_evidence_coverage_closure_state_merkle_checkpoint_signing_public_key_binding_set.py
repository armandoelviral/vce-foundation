from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet:
    """Preserve one canonical set of signing public-key bindings."""

    bindings: tuple[
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding,
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(self.bindings, tuple):
            raise TypeError("bindings must be a tuple")
        if not self.bindings:
            raise ValueError("bindings must not be empty")

        for binding in self.bindings:
            if not isinstance(
                binding,
                SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding,
            ):
                raise TypeError(
                    "bindings must contain only "
                    "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding "
                    "values"
                )

        key_ids = tuple(
            binding.signing_key_identity.key_id
            for binding in self.bindings
        )
        if len(set(key_ids)) != len(key_ids):
            raise ValueError(
                "bindings must contain unique key identifiers"
            )
        if key_ids != tuple(sorted(key_ids)):
            raise ValueError(
                "bindings must use canonical key identifier order"
            )

        fingerprints = tuple(
            binding
            .signing_key_identity
            .public_key_fingerprint
            for binding in self.bindings
        )
        if len(set(fingerprints)) != len(fingerprints):
            raise ValueError(
                "bindings must contain unique public-key fingerprints"
            )
