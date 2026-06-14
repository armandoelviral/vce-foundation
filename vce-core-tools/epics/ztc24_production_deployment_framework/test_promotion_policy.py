from epics.ztc24_production_deployment_framework.promotion_policy import (
    PromotionPolicy,
)


def test_allows_development_to_staging():

    policy = PromotionPolicy()

    assert policy.allow(
        source="development",
        target="staging",
    )


def test_allows_staging_to_production():

    policy = PromotionPolicy()

    assert policy.allow(
        source="staging",
        target="production",
    )


def test_rejects_development_to_production():

    policy = PromotionPolicy()

    assert not policy.allow(
        source="development",
        target="production",
    )


def test_rejects_unknown_environment():

    policy = PromotionPolicy()

    assert not policy.allow(
        source="sandbox",
        target="production",
    )
