from enum import StrEnum


class SecurityAdmissionAssessmentStatus(StrEnum):
    """Closed canonical states for one resolved admission assessment."""

    SATISFIED = "SATISFIED"
    NOT_SATISFIED = "NOT_SATISFIED"
    INDETERMINATE = "INDETERMINATE"
