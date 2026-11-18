import pytest

from sp001.infrastructure.product001_host_bootstrap import (
    create_app_from_environment,
)
from sp001.services.product001_commercial_startup_guard import (
    CommercialStartupBlockedError,
)


@pytest.mark.parametrize(
    "mode",
    ("production", "commercial", "staging-commercial"),
)
def test_commercial_bootstrap_is_blocked(mode):
    with pytest.raises(CommercialStartupBlockedError):
        create_app_from_environment(
            environment={"PRODUCT001_ENV": mode}
        )


def test_laboratory_bootstrap_is_allowed():
    app = create_app_from_environment(
        environment={"PRODUCT001_ENV": "laboratory"}
    )

    assert app is not None


def test_missing_environment_fails_closed():
    with pytest.raises(CommercialStartupBlockedError):
        create_app_from_environment(environment={})


def test_unknown_environment_fails_closed():
    with pytest.raises(CommercialStartupBlockedError):
        create_app_from_environment(
            environment={"PRODUCT001_ENV": "unknown"}
        )


def test_configuration_cannot_override_blocker():
    with pytest.raises(CommercialStartupBlockedError):
        create_app_from_environment(
            environment={
                "PRODUCT001_ENV": "production",
                "BLOCKER_HOST_001_OPEN": "false",
                "TRUST_ROOT_VERIFIED": "true",
            }
        )
