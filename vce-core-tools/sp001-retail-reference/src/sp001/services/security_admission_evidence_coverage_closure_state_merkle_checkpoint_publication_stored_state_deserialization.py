import json
from collections.abc import Iterable

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState,
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


_CHECKPOINT_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-MERKLE-CHECKPOINT"
)
_CHECKPOINT_KEYS = frozenset(
    {
        "domain",
        "origin",
        "root",
    }
)
_ROOT_KEYS = frozenset(
    {
        "algorithm",
        "tree_hash_profile",
        "leaf_count",
        "value",
    }
)


def deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state(
    *,
    stored_state: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState:
    """Reconstruct one publication state from strict canonical storage data."""

    if not isinstance(
        stored_state,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState,
    ):
        raise TypeError(
            "stored_state must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationStoredState"
        )

    try:
        checkpoint_data = json.loads(
            stored_state.checkpoint_serialization,
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

    root = SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot(
        algorithm=root_data["algorithm"],
        tree_hash_profile=root_data["tree_hash_profile"],
        leaf_count=root_data["leaf_count"],
        value=root_data["value"],
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
        != stored_state.checkpoint_serialization
    ):
        raise ValueError(
            "checkpoint_serialization must be canonical"
        )

    signing_key_identity = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity(
            key_id=stored_state.signing_key_id,
            algorithm=stored_state.signing_algorithm,
            public_key_encoding=(
                stored_state.public_key_encoding
            ),
            public_key_fingerprint=(
                stored_state.public_key_fingerprint
            ),
        )
    )
    checkpoint_signature = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature(
            checkpoint=checkpoint,
            signing_key_identity=signing_key_identity,
            signature_encoding=(
                stored_state.signature_encoding
            ),
            signature=stored_state.signature,
        )
    )
    publication_intent = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent(
            publication_id=stored_state.publication_id,
            checkpoint_signature=checkpoint_signature,
        )
    )

    return SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState(
        publication_intent=publication_intent,
        phase=(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase(
                stored_state.phase
            )
        ),
        revision=stored_state.revision,
    )


def _strict_json_object(
    pairs: Iterable[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}

    for key, value in pairs:
        if key in result:
            raise ValueError(
                "checkpoint_serialization must not "
                "contain duplicate keys"
            )
        result[key] = value

    return result


def _reject_json_constant(
    value: str,
) -> object:
    raise ValueError(
        "checkpoint_serialization must not contain "
        f"non-finite value {value}"
    )


def _require_exact_keys(
    *,
    value: object,
    expected: frozenset[str],
    field: str,
) -> None:
    if type(value) is not dict:
        raise TypeError(f"{field} must be a JSON object")
    if frozenset(value) != expected:
        raise ValueError(
            f"{field} must contain exactly the required keys"
        )
