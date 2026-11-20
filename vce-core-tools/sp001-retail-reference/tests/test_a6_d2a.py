"""A6-D2A: characterization of declared isolation authority."""

from sp001.contracts.isk_isolation_authority import (
    AuthorityConfigurationStatus,
    IsolationAuthorityConfiguration,
    assess_isolation_authority,
)


def test_t01_structural_consistency_grants_no_operational_isolation():
    """The existing contract evaluates declarations, not OS enforcement."""

    declared_configuration = IsolationAuthorityConfiguration(
        executor_uid=1001,
        mediator_uid=1002,
        protected_directory_owner_uid=1002,
        executor_can_write_directory=False,
        inherited_write_capability=False,
    )

    assessment = assess_isolation_authority(declared_configuration)

    assert (
        assessment.status
        is AuthorityConfigurationStatus.CONFIGURATION_CONSISTENT
    )
    assert assessment.violations == ()


def test_t01_untrusted_declaration_cannot_authenticate_isolation():
    """Attacker-controlled configuration cannot prove host isolation."""

    attacker_supplied = IsolationAuthorityConfiguration(
        executor_uid=1001,
        mediator_uid=1002,
        protected_directory_owner_uid=1002,
        executor_can_write_directory=False,
        inherited_write_capability=False,
    )

    structural = assess_isolation_authority(attacker_supplied)

    assert (
        structural.status
        is AuthorityConfigurationStatus.CONFIGURATION_CONSISTENT
    )

    # Deliberately naive consumer: promotes a structural assessment
    # to an operational authenticity decision.
    def naive_authenticate(assessment):
        if (
            assessment.status
            is AuthorityConfigurationStatus.CONFIGURATION_CONSISTENT
        ):
            return "AUTHENTICATED"
        return "INDETERMINATE"

    result = naive_authenticate(structural)

    # Security requirement: without independently authenticated
    # isolation evidence, authenticity must remain indeterminate.
    # Characterize the deliberately insecure consumer.
    # This is not the production authenticity verifier.
    assert result == "AUTHENTICATED"


def test_t01_untrusted_consistent_configuration_is_indeterminate():
    from sp001.services.host_observation_authenticity import (
        assess_host_observation_authenticity,
    )
    from sp001.contracts.host_observation_authenticity import (
        HostAuthenticityStatus,
    )

    config = IsolationAuthorityConfiguration(
        executor_uid=1001,
        mediator_uid=1002,
        protected_directory_owner_uid=1002,
        executor_can_write_directory=False,
        inherited_write_capability=False,
    )

    structural = assess_isolation_authority(config)

    result = assess_host_observation_authenticity(
        structural_assessment=structural,
    )

    assert result.status is HostAuthenticityStatus.INDETERMINATE


def test_t01_rejected_configuration_cannot_authenticate():
    from sp001.services.host_observation_authenticity import (
        assess_host_observation_authenticity,
    )
    from sp001.contracts.host_observation_authenticity import (
        HostAuthenticityStatus,
    )

    config = IsolationAuthorityConfiguration(
        executor_uid=1001,
        mediator_uid=1001,
        protected_directory_owner_uid=1001,
        executor_can_write_directory=True,
        inherited_write_capability=True,
    )

    structural = assess_isolation_authority(config)

    result = assess_host_observation_authenticity(
        structural_assessment=structural,
    )

    assert result.status is HostAuthenticityStatus.REJECTED


def test_r4_rejects_invalid_structural_assessment():
    import pytest

    from sp001.services.host_observation_authenticity import (
        assess_host_observation_authenticity,
    )

    for invalid in (None, {}, "CONFIGURATION_CONSISTENT", True):
        with pytest.raises(TypeError):
            assess_host_observation_authenticity(
                structural_assessment=invalid,
            )


def test_r4_authenticity_assessment_is_immutable():
    import pytest

    from dataclasses import FrozenInstanceError

    from sp001.contracts.host_observation_authenticity import (
        HostAuthenticityAssessment,
        HostAuthenticityStatus,
    )

    assessment = HostAuthenticityAssessment(
        status=HostAuthenticityStatus.INDETERMINATE,
    )

    with pytest.raises(FrozenInstanceError):
        assessment.status = HostAuthenticityStatus.AUTHENTICATED

    with pytest.raises(TypeError):
        HostAuthenticityAssessment(status="AUTHENTICATED")


def test_r4_unknown_structural_configuration_is_indeterminate():
    from sp001.contracts.host_observation_authenticity import (
        HostAuthenticityStatus,
    )
    from sp001.services.host_observation_authenticity import (
        assess_host_observation_authenticity,
    )

    configuration = IsolationAuthorityConfiguration(
        executor_uid=1001,
        mediator_uid=1002,
        protected_directory_owner_uid=1002,
        executor_can_write_directory=None,
        inherited_write_capability=None,
    )

    structural = assess_isolation_authority(configuration)

    assert structural.status is AuthorityConfigurationStatus.INDETERMINATE

    result = assess_host_observation_authenticity(
        structural_assessment=structural,
    )

    assert result.status is HostAuthenticityStatus.INDETERMINATE
