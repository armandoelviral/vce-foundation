"""A6-D2A: conservative host observation authenticity assessment.

Structural configuration is not evidence of operational isolation.
No authenticated outcome is available in this increment.
"""

from sp001.contracts.host_observation_authenticity import (
    HostAuthenticityAssessment,
    HostAuthenticityStatus,
)
from sp001.contracts.isk_isolation_authority import (
    AuthorityConfigurationAssessment,
    AuthorityConfigurationStatus,
)


def assess_host_observation_authenticity(
    *,
    structural_assessment: AuthorityConfigurationAssessment,
) -> HostAuthenticityAssessment:
    """Evaluate structural disqualification without granting authenticity."""

    if type(structural_assessment) is not AuthorityConfigurationAssessment:
        raise TypeError(
            "structural_assessment must be an AuthorityConfigurationAssessment"
        )

    if (
        structural_assessment.status
        is AuthorityConfigurationStatus.CONFIGURATION_REJECTED
    ):
        return HostAuthenticityAssessment(
            status=HostAuthenticityStatus.REJECTED,
        )

    return HostAuthenticityAssessment(
        status=HostAuthenticityStatus.INDETERMINATE,
    )
