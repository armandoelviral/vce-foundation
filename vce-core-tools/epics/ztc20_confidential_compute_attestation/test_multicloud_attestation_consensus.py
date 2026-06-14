from epics.ztc20_confidential_compute_attestation.multicloud_attestation_consensus import (
    MultiCloudAttestationConsensus,
)


def test_two_of_three_attested_reaches_consensus():

    consensus = MultiCloudAttestationConsensus()

    assert consensus.has_consensus(
        total_witnesses=3,
        attested_witnesses=2,
    )


def test_one_of_three_attested_fails_consensus():

    consensus = MultiCloudAttestationConsensus()

    assert not consensus.has_consensus(
        total_witnesses=3,
        attested_witnesses=1,
    )


def test_three_of_three_attested_reaches_consensus():

    consensus = MultiCloudAttestationConsensus()

    assert consensus.has_consensus(
        total_witnesses=3,
        attested_witnesses=3,
    )


def test_three_of_five_attested_reaches_consensus():

    consensus = MultiCloudAttestationConsensus()

    assert consensus.has_consensus(
        total_witnesses=5,
        attested_witnesses=3,
    )
