from phase4.reputation_constitution_layer.reputation_claim import (
    ReputationClaim,
)

from phase4.reputation_constitution_layer.reputation_evidence import (
    ReputationEvidence,
)

from phase4.reputation_constitution_layer.reputation_accrual import (
    ReputationAccrual,
)

from phase4.reputation_constitution_layer.reputation_loss import (
    ReputationLoss,
)

from phase4.reputation_constitution_layer.reputation_appeal import (
    ReputationAppeal,
)

from phase4.reputation_constitution_layer.reputation_state import (
    ReputationState,
)

from phase4.reputation_constitution_layer.reputation_verifier import (
    ReputationVerifier,
)


class ReputationFlow:

    @staticmethod
    def generate():

        claim = ReputationClaim(
            identity_id="identity-001",
            claim_type="duty_compliance",
        )

        evidence = ReputationEvidence(
            claim_id="claim-001",
            evidence_hash="hash-001",
        )

        accrual = ReputationAccrual(
            identity_id="identity-001",
            points=100,
        )

        loss = ReputationLoss(
            identity_id="identity-001",
            points=5,
        )

        appeal = ReputationAppeal(
            appeal_id="appeal-001",
            reputation_event="loss-001",
        )

        state = ReputationState(
            score=95,
        )

        valid = ReputationVerifier.verify(
            state
        )

        return {
            "claim":
                claim.to_dict(),
            "evidence":
                evidence.to_dict(),
            "accrual":
                accrual.to_dict(),
            "loss":
                loss.to_dict(),
            "appeal":
                appeal.to_dict(),
            "state":
                state.to_dict(),
            "valid":
                valid,
        }
