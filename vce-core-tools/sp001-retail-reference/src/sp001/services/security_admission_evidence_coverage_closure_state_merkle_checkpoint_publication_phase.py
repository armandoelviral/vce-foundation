from enum import StrEnum


class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase(
    StrEnum
):
    """Canonical durable phases for one checkpoint publication."""

    INTENT_RECORDED = "INTENT_RECORDED"
    PREPARED = "PREPARED"
    COMMIT_DECIDED = "COMMIT_DECIDED"
    COMMITTED = "COMMITTED"
    ABORT_DECIDED = "ABORT_DECIDED"
    ABORTED = "ABORTED"
