from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state import (
    SECURITY_ADMISSION_CHECKPOINT_PUBLICATION_STORAGE_SCHEMA_VERSION,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint,
)


PublicationState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
)
StoredState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState
)


def project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state(
    *,
    state: PublicationState,
) -> StoredState:
    """Project one validated publication state to primitive storage fields."""

    if not isinstance(state, PublicationState):
        raise TypeError(
            "state must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationState"
        )

    intent = state.publication_intent
    checkpoint_signature = intent.checkpoint_signature
    signing_key_identity = (
        checkpoint_signature.signing_key_identity
    )

    checkpoint_serialization = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=checkpoint_signature.checkpoint,
        )
    )

    return StoredState(
        storage_schema_version=(
            SECURITY_ADMISSION_CHECKPOINT_PUBLICATION_STORAGE_SCHEMA_VERSION
        ),
        publication_id=intent.publication_id,
        checkpoint_serialization=checkpoint_serialization,
        signing_key_id=signing_key_identity.key_id,
        signing_algorithm=signing_key_identity.algorithm,
        public_key_encoding=(
            signing_key_identity.public_key_encoding
        ),
        public_key_fingerprint=(
            signing_key_identity.public_key_fingerprint
        ),
        signature_encoding=(
            checkpoint_signature.signature_encoding
        ),
        signature=checkpoint_signature.signature,
        phase=state.phase.value,
        revision=state.revision,
    )
