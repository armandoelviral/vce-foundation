from phase4.inter_institution_federation_layer.inter_institution_trust import (
    InterInstitutionTrust,
)


def test_contains_source():

    trust = InterInstitutionTrust(
        source_institution="inst-001",
        target_institution="inst-002",
        trusted=True,
    )

    assert (
        trust.source_institution
        == "inst-001"
    )


def test_contains_target():

    trust = InterInstitutionTrust(
        source_institution="inst-001",
        target_institution="inst-002",
        trusted=True,
    )

    assert (
        trust.target_institution
        == "inst-002"
    )


def test_contains_trust_flag():

    trust = InterInstitutionTrust(
        source_institution="inst-001",
        target_institution="inst-002",
        trusted=True,
    )

    assert trust.trusted is True


def test_serializes():

    trust = InterInstitutionTrust(
        source_institution="inst-001",
        target_institution="inst-002",
        trusted=True,
    )

    assert trust.to_dict() == {
        "source_institution":
            "inst-001",
        "target_institution":
            "inst-002",
        "trusted":
            True,
    }
