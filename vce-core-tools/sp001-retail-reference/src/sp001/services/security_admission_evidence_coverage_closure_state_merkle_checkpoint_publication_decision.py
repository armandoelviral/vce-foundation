from enum import StrEnum


class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision(
    StrEnum
):
    """Identify one nominal global checkpoint-publication decision."""

    COMMIT = "COMMIT"
    ABORT = "ABORT"
