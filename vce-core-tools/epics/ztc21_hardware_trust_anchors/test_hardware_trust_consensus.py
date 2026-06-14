from epics.ztc21_hardware_trust_anchors.hardware_trust_consensus import (
    HardwareTrustConsensus,
)


def test_two_of_three_trusted_reaches_consensus():

    consensus = HardwareTrustConsensus()

    assert consensus.has_consensus(
        total_providers=3,
        trusted_providers=2,
    )


def test_one_of_three_trusted_fails_consensus():

    consensus = HardwareTrustConsensus()

    assert not consensus.has_consensus(
        total_providers=3,
        trusted_providers=1,
    )


def test_three_of_three_trusted_reaches_consensus():

    consensus = HardwareTrustConsensus()

    assert consensus.has_consensus(
        total_providers=3,
        trusted_providers=3,
    )


def test_three_of_five_trusted_reaches_consensus():

    consensus = HardwareTrustConsensus()

    assert consensus.has_consensus(
        total_providers=5,
        trusted_providers=3,
    )
