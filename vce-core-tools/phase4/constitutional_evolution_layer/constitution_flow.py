from phase4.constitutional_evolution_layer.constitution_proposal import (
    ConstitutionProposal,
)

from phase4.constitutional_evolution_layer.constitution_amendment import (
    ConstitutionAmendment,
)

from phase4.constitutional_evolution_layer.ratification_vote import (
    RatificationVote,
)

from phase4.constitutional_evolution_layer.constitution_version import (
    ConstitutionVersion,
)

from phase4.constitutional_evolution_layer.constitution_state import (
    ConstitutionState,
)

from phase4.constitutional_evolution_layer.constitution_history import (
    ConstitutionHistory,
)

from phase4.constitutional_evolution_layer.constitution_verifier import (
    ConstitutionVerifier,
)


class ConstitutionFlow:

    @staticmethod
    def generate():

        proposal = ConstitutionProposal(
            proposal_id="const-proposal-001",
            title="Ratify Principle #7",
            status="PROPOSED",
        )

        amendment = ConstitutionAmendment(
            amendment_id="amendment-001",
            proposal_id=proposal.proposal_id,
        )

        ratification = RatificationVote(
            amendment_id=amendment.amendment_id,
            approved=True,
        )

        version = ConstitutionVersion(
            version="v2.0",
        )

        state = ConstitutionState(
            constitution_state="AMENDED",
        )

        history = ConstitutionHistory(
            versions=[
                "v1.0",
                version.version,
            ],
        )

        valid = ConstitutionVerifier.verify(
            state
        )

        return {
            "proposal":
                proposal.to_dict(),
            "amendment":
                amendment.to_dict(),
            "ratification":
                ratification.to_dict(),
            "version":
                version.to_dict(),
            "state":
                state.to_dict(),
            "history":
                history.to_dict(),
            "valid":
                valid,
        }
