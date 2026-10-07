from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint,
)


PublicationIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent
)
StoredIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent
)
_STORAGE_SCHEMA_VERSION = 1


def project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
    *,
    publication_intent: PublicationIntent,
) -> StoredIntent:
    """Project one signed publication intent into portable stored values."""

    if not isinstance(
        publication_intent,
        PublicationIntent,
    ):
        raise TypeError(
            "publication_intent must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationIntent"
        )

    checkpoint_signature = (
        publication_intent
        .checkpoint_signature
    )
    signing_key_identity = (
        checkpoint_signature
        .signing_key_identity
    )

    return StoredIntent(
        storage_schema_version=_STORAGE_SCHEMA_VERSION,
        publication_id=(
            publication_intent.publication_id
        ),
        checkpoint_serialization=(
            serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
                checkpoint=(
                    checkpoint_signature.checkpoint
                ),
            )
        ),
        signing_key_id=(
            signing_key_identity.key_id
        ),
        signing_algorithm=(
            signing_key_identity.algorithm
        ),
        public_key_encoding=(
            signing_key_identity
            .public_key_encoding
        ),
        public_key_fingerprint=(
            signing_key_identity
            .public_key_fingerprint
        ),
        signature_encoding=(
            checkpoint_signature.signature_encoding
        ),
        signature=checkpoint_signature.signature,
    )
