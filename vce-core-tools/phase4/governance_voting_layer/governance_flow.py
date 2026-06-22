from phase4.governance_voting_layer.governance_proposal import (
    GovernanceProposal,
)

from phase4.governance_voting_layer.vote_record import (
    VoteRecord,
)

from phase4.governance_voting_layer.vote_tally import (
    VoteTally,
)

from phase4.governance_voting_layer.consensus_decision import (
    ConsensusDecision,
)

from phase4.governance_voting_layer.governance_state import (
    GovernanceState,
)

from phase4.governance_voting_layer.governance_verifier import (
    GovernanceVerifier,
)


class GovernanceFlow:

    @staticmethod
    def generate():

        proposal = GovernanceProposal(
            proposal_id="proposal-001",
            title="Increase minimum reputation requirement",
        )

        votes = [
            VoteRecord(
                citizen_did="did:tcn:test:01",
                proposal_id="proposal-001",
                vote="YES",
            ),
            VoteRecord(
                citizen_did="did:tcn:test:02",
                proposal_id="proposal-001",
                vote="YES",
            ),
            VoteRecord(
                citizen_did="did:tcn:test:03",
                proposal_id="proposal-001",
                vote="NO",
            ),
        ]

        tally = VoteTally.calculate(
            proposal_id="proposal-001",
            votes=votes,
        )

        decision = (
            ConsensusDecision.decide(
                tally
            )
        )

        state = GovernanceState(
            governance_state="UPDATED",
        )

        valid = (
            GovernanceVerifier.verify(
                state
            )
        )

        return {
            "proposal":
                proposal.to_dict(),
            "votes": [
                vote.to_dict()
                for vote in votes
            ],
            "tally":
                tally,
            "decision":
                decision,
            "state":
                state.to_dict(),
            "valid":
                valid,
        }
