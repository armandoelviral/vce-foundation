from epics.epic085_policy_authority_layer.policy_versioning import (
    PolicyVersioning,
)


def test_policy_versioning_adds_version():

    versioning = PolicyVersioning()

    versioning.add_version(
        "clinical-admission-policy",
        "1.0.0",
    )

    assert versioning.versions_for(
        "clinical-admission-policy"
    ) == ["1.0.0"]


def test_policy_versioning_tracks_multiple_versions():

    versioning = PolicyVersioning()

    versioning.add_version(
        "clinical-admission-policy",
        "1.0.0",
    )

    versioning.add_version(
        "clinical-admission-policy",
        "1.1.0",
    )

    assert versioning.versions_for(
        "clinical-admission-policy"
    ) == [
        "1.0.0",
        "1.1.0",
    ]


def test_policy_versioning_returns_latest_version():

    versioning = PolicyVersioning()

    versioning.add_version(
        "clinical-admission-policy",
        "1.0.0",
    )

    versioning.add_version(
        "clinical-admission-policy",
        "1.1.0",
    )

    assert (
        versioning.latest_version(
            "clinical-admission-policy"
        )
        == "1.1.0"
    )


def test_policy_versioning_returns_none_for_unknown_policy():

    versioning = PolicyVersioning()

    assert (
        versioning.latest_version(
            "unknown-policy"
        )
        is None
    )
