from epics.ztc13_transparency_federation.transparency_anchor import (
    TransparencyAnchor,
)


def test_anchor_contains_attestation():

    anchor = TransparencyAnchor(
        attestation_id="att-001",
        anchor_id="anchor-001",
        transparency_root="root-001",
    )

    assert anchor.attestation_id == "att-001"


def test_anchor_contains_anchor_id():

    anchor = TransparencyAnchor(
        attestation_id="att-001",
        anchor_id="anchor-001",
        transparency_root="root-001",
    )

    assert anchor.anchor_id == "anchor-001"


def test_anchor_contains_transparency_root():

    anchor = TransparencyAnchor(
        attestation_id="att-001",
        anchor_id="anchor-001",
        transparency_root="root-001",
    )

    assert anchor.transparency_root == "root-001"
