from phase4.inter_institution_federation_layer.delegated_authority import (
    DelegatedAuthority,
)


def test_contains_source():

    delegation = DelegatedAuthority(
        source_institution="inst-001",
        target_institution="inst-002",
        authority="adjudication_review",
    )

    assert (
        delegation.source_institution
        == "inst-001"
    )


def test_contains_target():

    delegation = DelegatedAuthority(
        source_institution="inst-001",
        target_institution="inst-002",
        authority="adjudication_review",
    )

    assert (
        delegation.target_institution
        == "inst-002"
    )


def test_contains_authority():

    delegation = DelegatedAuthority(
        source_institution="inst-001",
        target_institution="inst-002",
        authority="adjudication_review",
    )

    assert (
        delegation.authority
        == "adjudication_review"
    )


def test_serializes():

    delegation = DelegatedAuthority(
        source_institution="inst-001",
        target_institution="inst-002",
        authority="adjudication_review",
    )

    assert delegation.to_dict() == {
        "source_institution":
            "inst-001",
        "target_institution":
            "inst-002",
        "authority":
            "adjudication_review",
    }
