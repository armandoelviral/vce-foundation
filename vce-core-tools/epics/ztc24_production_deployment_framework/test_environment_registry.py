from epics.ztc24_production_deployment_framework.environment_registry import (
    EnvironmentRegistry,
)


def test_registry_starts_empty():

    registry = EnvironmentRegistry()

    assert registry.count() == 0


def test_registry_adds_environment():

    registry = EnvironmentRegistry()

    registry.add(
        "staging"
    )

    assert registry.count() == 1


def test_registry_reports_known_environment():

    registry = EnvironmentRegistry()

    registry.add(
        "production"
    )

    assert registry.exists(
        "production"
    )


def test_registry_returns_false_for_unknown_environment():

    registry = EnvironmentRegistry()

    assert not registry.exists(
        "sandbox"
    )
