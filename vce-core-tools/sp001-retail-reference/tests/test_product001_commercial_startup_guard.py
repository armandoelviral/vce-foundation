import pytest

from sp001.services.product001_commercial_startup_guard import (
    CommercialStartupBlockedError,
    authorize_product001_startup,
)


@pytest.mark.parametrize(
    "environment",
    ("production", "commercial", "staging-commercial"),
)
@pytest.mark.parametrize(
    "trust_root_verified",
    (False, True),
)
def test_open_blocker_denies_commercial_startup(
    environment,
    trust_root_verified,
):
    with pytest.raises(CommercialStartupBlockedError):
        authorize_product001_startup(
            environment=environment,
            trust_root_verified=trust_root_verified,
        )


@pytest.mark.parametrize(
    "trust_root_verified",
    (False, True),
)
def test_laboratory_startup_is_permitted(
    trust_root_verified,
):
    result = authorize_product001_startup(
        environment="laboratory",
        trust_root_verified=trust_root_verified,
    )

    assert result is True


@pytest.mark.parametrize(
    "environment",
    ("", "unknown", "PRODUCTION", None),
)
def test_unknown_environment_fails_closed(environment):
    with pytest.raises(
        (CommercialStartupBlockedError, TypeError, ValueError)
    ):
        authorize_product001_startup(
            environment=environment,
            trust_root_verified=False,
        )


def test_untrusted_configuration_type_is_rejected():
    with pytest.raises(TypeError):
        authorize_product001_startup(
            environment="laboratory",
            trust_root_verified="true",
        )
