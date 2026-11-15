import pytest

from sp001.contracts.isk_isolation_authority import (
    AuthorityConfigurationStatus,
    AuthorityViolation,
    IsolationAuthorityConfiguration,
    assess_isolation_authority,
)


def configuration(**overrides):
    values = {
        "executor_uid": 1001,
        "mediator_uid": 1002,
        "protected_directory_owner_uid": 1002,
        "executor_can_write_directory": False,
        "inherited_write_capability": False,
    }
    values.update(overrides)
    return IsolationAuthorityConfiguration(**values)


def test_consistent_configuration():
    result = assess_isolation_authority(configuration())
    assert result.status is AuthorityConfigurationStatus.CONFIGURATION_CONSISTENT
    assert result.violations == ()


@pytest.mark.parametrize(
    ("overrides", "violation"),
    [
        (
            {"mediator_uid": 1001},
            AuthorityViolation.SAME_IDENTITY,
        ),
        (
            {"protected_directory_owner_uid": 1001},
            AuthorityViolation.EXECUTOR_OWNS_DIRECTORY,
        ),
        (
            {"executor_can_write_directory": True},
            AuthorityViolation.EXECUTOR_CAN_WRITE_DIRECTORY,
        ),
        (
            {"inherited_write_capability": True},
            AuthorityViolation.INHERITED_WRITE_CAPABILITY,
        ),
    ],
)
def test_rejects_unsafe_configuration(overrides, violation):
    result = assess_isolation_authority(configuration(**overrides))
    assert result.status is AuthorityConfigurationStatus.CONFIGURATION_REJECTED
    assert violation in result.violations


@pytest.mark.parametrize(
    "field",
    ["executor_can_write_directory", "inherited_write_capability"],
)
def test_unknown_control_is_indeterminate(field):
    result = assess_isolation_authority(configuration(**{field: None}))
    assert result.status is AuthorityConfigurationStatus.INDETERMINATE


def test_known_violation_takes_precedence_over_unknown():
    result = assess_isolation_authority(
        configuration(
            mediator_uid=1001,
            inherited_write_capability=None,
        )
    )
    assert result.status is AuthorityConfigurationStatus.CONFIGURATION_REJECTED


@pytest.mark.parametrize(
    "field",
    ["executor_uid", "mediator_uid", "protected_directory_owner_uid"],
)
@pytest.mark.parametrize("invalid", [-1, True, "1001"])
def test_rejects_invalid_identity(field, invalid):
    with pytest.raises((ValueError, TypeError)):
        configuration(**{field: invalid})


@pytest.mark.parametrize(
    "field",
    ["executor_can_write_directory", "inherited_write_capability"],
)
def test_rejects_invalid_control_type(field):
    with pytest.raises(TypeError):
        configuration(**{field: 1})


def test_rejects_wrong_contract_type():
    with pytest.raises(TypeError):
        assess_isolation_authority(None)


def test_assessment_is_immutable():
    result = assess_isolation_authority(configuration())
    with pytest.raises(AttributeError):
        result.status = AuthorityConfigurationStatus.CONFIGURATION_REJECTED


@pytest.mark.parametrize(
    ("status", "violations"),
    [
        (
            AuthorityConfigurationStatus.CONFIGURATION_CONSISTENT,
            (AuthorityViolation.SAME_IDENTITY,),
        ),
        (
            AuthorityConfigurationStatus.CONFIGURATION_REJECTED,
            (),
        ),
        (
            AuthorityConfigurationStatus.INDETERMINATE,
            (AuthorityViolation.EXECUTOR_OWNS_DIRECTORY,),
        ),
    ],
)
def test_rejects_contradictory_assessment(status, violations):
    from sp001.contracts.isk_isolation_authority import (
        AuthorityConfigurationAssessment,
    )

    with pytest.raises(ValueError):
        AuthorityConfigurationAssessment(
            status=status,
            violations=violations,
        )


def test_rejects_duplicate_assessment_violations():
    from sp001.contracts.isk_isolation_authority import (
        AuthorityConfigurationAssessment,
    )

    with pytest.raises(ValueError):
        AuthorityConfigurationAssessment(
            status=AuthorityConfigurationStatus.CONFIGURATION_REJECTED,
            violations=(
                AuthorityViolation.SAME_IDENTITY,
                AuthorityViolation.SAME_IDENTITY,
            ),
        )


@pytest.mark.parametrize(
    ("status", "violations"),
    [
        ("CONFIGURATION_CONSISTENT", ()),
        (AuthorityConfigurationStatus.CONFIGURATION_CONSISTENT, []),
        (
            AuthorityConfigurationStatus.CONFIGURATION_REJECTED,
            ("SAME_IDENTITY",),
        ),
    ],
)
def test_rejects_invalid_assessment_types(status, violations):
    from sp001.contracts.isk_isolation_authority import (
        AuthorityConfigurationAssessment,
    )

    with pytest.raises(TypeError):
        AuthorityConfigurationAssessment(
            status=status,
            violations=violations,
        )
