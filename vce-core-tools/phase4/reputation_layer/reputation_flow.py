from phase4.reputation_layer.reputation_event import (
    ReputationEvent,
)

from phase4.reputation_layer.reputation_score import (
    ReputationScore,
)

from phase4.reputation_layer.reputation_state import (
    ReputationState,
)

from phase4.reputation_layer.reputation_verifier import (
    ReputationVerifier,
)


class ReputationFlow:

    @staticmethod
    def generate():

        events = [
            ReputationEvent(
                citizen_did="did:tcn:test:01",
                event_type="response_valid",
                impact=10,
            ),
            ReputationEvent(
                citizen_did="did:tcn:test:01",
                event_type="governance_participation",
                impact=15,
            ),
            ReputationEvent(
                citizen_did="did:tcn:test:01",
                event_type="response_recovery",
                impact=20,
            ),
        ]

        score_value = sum(
            event.impact
            for event in events
        )

        score = ReputationScore(
            citizen_did="did:tcn:test:01",
            score=score_value,
        )

        state = ReputationState(
            citizen_did="did:tcn:test:01",
            reputation_state="TRUSTED",
        )

        trusted = ReputationVerifier.verify(
            state
        )

        return {
            "events": [
                event.to_dict()
                for event in events
            ],
            "score": score.to_dict(),
            "state": state.to_dict(),
            "trusted": trusted,
        }
