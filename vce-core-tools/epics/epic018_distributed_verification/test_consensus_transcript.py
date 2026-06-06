from epics.epic018_distributed_verification.consensus_transcript import (
    ConsensusTranscript,
)


def test_consensus_transcript_can_be_verified():

    builder = ConsensusTranscript()

    proof = builder.create(
        artifact_hash="abc123",
        votes={
            "node_a": True,
            "node_b": True,
        },
        quorum_result=True,
    )

    assert builder.verify(proof) is True


def test_consensus_transcript_rejects_tampering():

    builder = ConsensusTranscript()

    proof = builder.create(
        artifact_hash="abc123",
        votes={
            "node_a": True,
            "node_b": True,
        },
        quorum_result=True,
    )

    proof["transcript"]["artifact_hash"] = "tampered"

    assert builder.verify(proof) is False
