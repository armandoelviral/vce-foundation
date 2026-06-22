from phase4.constitutional_evolution_layer.constitution_version import (
    ConstitutionVersion,
)


def test_contains_version():

    version = ConstitutionVersion(
        version="v1.0",
    )

    assert version.version == "v1.0"


def test_serializes():

    version = ConstitutionVersion(
        version="v1.0",
    )

    assert version.to_dict() == {
        "version":
            "v1.0",
    }


def test_supports_next_version():

    version = ConstitutionVersion(
        version="v2.0",
    )

    assert version.version == "v2.0"
