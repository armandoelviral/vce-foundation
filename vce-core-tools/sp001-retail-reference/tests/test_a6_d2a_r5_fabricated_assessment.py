"""R5-D9B: public construction does not establish authority."""

from sp001.contracts.host_observation_authenticity import (
    HostAuthenticityAssessment,
    HostAuthenticityStatus,
)


def test_positive_assessment_is_publicly_constructible():
    fabricated = HostAuthenticityAssessment(
        status=HostAuthenticityStatus.AUTHENTICATED,
    )

    assert fabricated.status is HostAuthenticityStatus.AUTHENTICATED
