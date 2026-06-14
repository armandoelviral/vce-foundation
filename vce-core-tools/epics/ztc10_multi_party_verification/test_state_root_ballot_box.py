from epics.ztc10_multi_party_verification.state_root_ballot_box import (
    StateRootBallotBox,
)

from epics.ztc10_multi_party_verification.witness_response import (
    WitnessResponse,
)


def test_groups_responses_by_state_root():

    responses = [
        WitnessResponse(
            witness_id="witness-001",
            state_root_hash="root-a",
            classical_signature="sig-a1",
            pqc_signature="pqc-a1",
            accepted=True,
        ),
        WitnessResponse(
            witness_id="witness-002",
            state_root_hash="root-a",
            classical_signature="sig-a2",
            pqc_signature="pqc-a2",
            accepted=True,
        ),
    ]

    ballot = StateRootBallotBox.group(
        responses
    )

    assert len(ballot["root-a"]) == 2


def test_separates_different_state_roots():

    responses = [
        WitnessResponse(
            witness_id="witness-001",
            state_root_hash="root-a",
            classical_signature="sig-a1",
            pqc_signature="pqc-a1",
            accepted=True,
        ),
        WitnessResponse(
            witness_id="witness-002",
            state_root_hash="root-b",
            classical_signature="sig-b1",
            pqc_signature="pqc-b1",
            accepted=True,
        ),
    ]

    ballot = StateRootBallotBox.group(
        responses
    )

    assert len(ballot["root-a"]) == 1
    assert len(ballot["root-b"]) == 1
