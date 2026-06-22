from phase4.constitutional_evolution_layer.constitution_history import (
    ConstitutionHistory,
)


def test_contains_versions():

    history = ConstitutionHistory(
        versions=[
            "v1.0",
            "v2.0",
        ],
    )

    assert len(history.versions) == 2


def test_contains_latest_version():

    history = ConstitutionHistory(
        versions=[
            "v1.0",
            "v2.0",
        ],
    )

    assert history.latest_version() == "v2.0"


def test_serializes():

    history = ConstitutionHistory(
        versions=[
            "v1.0",
            "v2.0",
        ],
    )

    assert history.to_dict() == {
        "versions": [
            "v1.0",
            "v2.0",
        ],
        "latest_version": "v2.0",
    }
