from dataclasses import dataclass
from enum import Enum


class AuthorityConfigurationStatus(str, Enum):
    CONFIGURATION_CONSISTENT = "CONFIGURATION_CONSISTENT"
    CONFIGURATION_REJECTED = "CONFIGURATION_REJECTED"
    INDETERMINATE = "INDETERMINATE"


class AuthorityViolation(str, Enum):
    SAME_IDENTITY = "SAME_IDENTITY"
    EXECUTOR_OWNS_DIRECTORY = "EXECUTOR_OWNS_DIRECTORY"
    EXECUTOR_CAN_WRITE_DIRECTORY = "EXECUTOR_CAN_WRITE_DIRECTORY"
    INHERITED_WRITE_CAPABILITY = "INHERITED_WRITE_CAPABILITY"


@dataclass(frozen=True, slots=True)
class IsolationAuthorityConfiguration:
    executor_uid: int
    mediator_uid: int
    protected_directory_owner_uid: int
    executor_can_write_directory: bool | None
    inherited_write_capability: bool | None

    def __post_init__(self) -> None:
        for name in (
            "executor_uid",
            "mediator_uid",
            "protected_directory_owner_uid",
        ):
            value = getattr(self, name)
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be a nonnegative integer")

        for name in (
            "executor_can_write_directory",
            "inherited_write_capability",
        ):
            value = getattr(self, name)
            if value is not None and type(value) is not bool:
                raise TypeError(f"{name} must be bool or None")


@dataclass(frozen=True, slots=True)
class AuthorityConfigurationAssessment:
    status: AuthorityConfigurationStatus
    violations: tuple[AuthorityViolation, ...]

    def __post_init__(self) -> None:
        if type(self.status) is not AuthorityConfigurationStatus:
            raise TypeError(
                "status must be an AuthorityConfigurationStatus"
            )

        if type(self.violations) is not tuple:
            raise TypeError("violations must be an immutable tuple")

        if any(
            type(violation) is not AuthorityViolation
            for violation in self.violations
        ):
            raise TypeError(
                "each violation must be an AuthorityViolation"
            )

        if len(set(self.violations)) != len(self.violations):
            raise ValueError("duplicate authority violation")

        if (
            self.status is AuthorityConfigurationStatus.CONFIGURATION_REJECTED
        ):
            if not self.violations:
                raise ValueError(
                    "rejected configuration requires violations"
                )
        elif self.violations:
            raise ValueError(
                "non-rejected configuration cannot contain violations"
            )


def assess_isolation_authority(
    config: IsolationAuthorityConfiguration,
) -> AuthorityConfigurationAssessment:
    if type(config) is not IsolationAuthorityConfiguration:
        raise TypeError("Expected IsolationAuthorityConfiguration")

    violations = []

    if config.executor_uid == config.mediator_uid:
        violations.append(AuthorityViolation.SAME_IDENTITY)

    if config.executor_uid == config.protected_directory_owner_uid:
        violations.append(AuthorityViolation.EXECUTOR_OWNS_DIRECTORY)

    if config.executor_can_write_directory is True:
        violations.append(AuthorityViolation.EXECUTOR_CAN_WRITE_DIRECTORY)

    if config.inherited_write_capability is True:
        violations.append(AuthorityViolation.INHERITED_WRITE_CAPABILITY)

    if violations:
        status = AuthorityConfigurationStatus.CONFIGURATION_REJECTED
    elif (
        config.executor_can_write_directory is None
        or config.inherited_write_capability is None
    ):
        status = AuthorityConfigurationStatus.INDETERMINATE
    else:
        status = AuthorityConfigurationStatus.CONFIGURATION_CONSISTENT

    return AuthorityConfigurationAssessment(
        status=status,
        violations=tuple(violations),
    )
