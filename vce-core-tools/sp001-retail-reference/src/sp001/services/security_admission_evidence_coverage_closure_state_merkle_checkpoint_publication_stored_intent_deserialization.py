import json

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_root import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
)


StoredIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent
)
PublicationIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent
)
_SUPPORTED_STORAGE_SCHEMA_VERSION = 1
_CHECKPOINT_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-MERKLE-CHECKPOINT"
)
_CHECKPOINT_KEYS = {
    "domain",
    "origin",
    "root",
}
_ROOT_KEYS = {
    "algorithm",
    "leaf_count",
    "tree_hash_profile",
    "value",
}


def deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
    *,
    stored_intent: StoredIntent,
) -> PublicationIntent:
    """Reconstruct one signed publication intent from strict portable values."""

    if not isinstance(
        stored_intent,
        StoredIntent,
    ):
        raise TypeError(
            "stored_intent must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationStoredIntent"
        )

    if (
        stored_intent.storage_schema_version
        != _SUPPORTED_STORAGE_SCHEMA_VERSION
    ):
        raise ValueError(
            "stored intent uses an unsupported "
            "storage schema version"
        )

    try:
        checkpoint_data = json.loads(
            stored_intent.checkpoint_serialization,
            object_pairs_hook=_strict_json_object,
            parse_constant=_reject_json_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError(
            "checkpoint_serialization must contain valid JSON"
        ) from error

    _require_exact_keys(
        value=checkpoint_data,
        expected=_CHECKPOINT_KEYS,
        field="checkpoint",
    )

    if checkpoint_data["domain"] != _CHECKPOINT_DOMAIN:
        raise ValueError(
            "checkpoint domain is not supported"
        )

    root_data = checkpoint_data["root"]
    _require_exact_keys(
        value=root_data,
        expected=_ROOT_KEYS,
        field="checkpoint root",
    )

    root = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot(
            algorithm=root_data["algorithm"],
            tree_hash_profile=(
                root_data["tree_hash_profile"]
            ),
            leaf_count=root_data["leaf_count"],
            value=root_data["value"],
        )
    )
    checkpoint = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint(
            origin=checkpoint_data["origin"],
            root=root,
        )
    )

    canonical_checkpoint = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=checkpoint,
        )
    )
    if (
        canonical_checkpoint
        != stored_intent.checkpoint_serialization
    ):
        raise ValueError(
            "checkpoint_serialization must be canonical"
        )

    signing_key_identity = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity(
            key_id=stored_intent.signing_key_id,
            algorithm=stored_intent.signing_algorithm,
            public_key_encoding=(
                stored_intent.public_key_encoding
            ),
            public_key_fingerprint=(
                stored_intent.public_key_fingerprint
            ),
        )
    )
    checkpoint_signature = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature(
            checkpoint=checkpoint,
            signing_key_identity=signing_key_identity,
            signature_encoding=(
                stored_intent.signature_encoding
            ),
            signature=stored_intent.signature,
        )
    )

    return PublicationIntent(
        publication_id=stored_intent.publication_id,
        checkpoint_signature=checkpoint_signature,
    )


def _strict_json_object(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    value: dict[str, object] = {}

    for key, item in pairs:
        if key in value:
            raise ValueError(
                "checkpoint_serialization must not "
                "contain duplicate object keys"
            )
        value[key] = item

    return value


def _reject_json_constant(
    value: str,
) -> object:
    raise ValueError(
        "checkpoint_serialization must not contain "
        f"non-finite JSON constant {value}"
    )


def _require_exact_keys(
    *,
    value: object,
    expected: set[str],
    field: str,
) -> None:
    if type(value) is not dict:
        raise TypeError(
            f"{field} must be a JSON object"
        )
    if set(value) != expected:
        raise ValueError(
            f"{field} must contain exact canonical keys"
        )
