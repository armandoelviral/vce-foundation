import json

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)


StoredEvidence = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence
)
_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
    "MERKLE-CHECKPOINT-PUBLICATION-DECISION-EVIDENCE"
)
_STORAGE_SCHEMA_VERSION = 1


def serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
    *,
    stored_evidence: StoredEvidence,
) -> str:
    """Serialize durable signed decision evidence canonically."""

    if not isinstance(
        stored_evidence,
        StoredEvidence,
    ):
        raise TypeError(
            "stored_evidence must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationDecisionStoredEvidence"
        )

    publication_intent = json.loads(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            stored_intent=(
                stored_evidence.publication_intent
            ),
        )
    )
    decision_record = json.loads(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record(
            stored_record=(
                stored_evidence.decision_record
            ),
        )
    )

    document = {
        "decision_record": decision_record,
        "domain": _DOMAIN,
        "publication_intent": publication_intent,
        "storage_schema_version": (
            _STORAGE_SCHEMA_VERSION
        ),
    }

    return json.dumps(
        document,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
