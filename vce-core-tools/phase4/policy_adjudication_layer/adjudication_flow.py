from phase4.policy_adjudication_layer.conflict_detection import (
    ConflictDetection,
)

from phase4.policy_adjudication_layer.policy_precedence import (
    PolicyPrecedence,
)

from phase4.policy_adjudication_layer.exception_handling import (
    ExceptionHandling,
)

from phase4.policy_adjudication_layer.appeal_record import (
    AppealRecord,
)

from phase4.policy_adjudication_layer.dispute_resolution import (
    DisputeResolution,
)

from phase4.policy_adjudication_layer.adjudication_state import (
    AdjudicationState,
)

from phase4.policy_adjudication_layer.adjudication_verifier import (
    AdjudicationVerifier,
)


class AdjudicationFlow:

    @staticmethod
    def generate():

        conflict = (
            ConflictDetection.detect(
                policy_a="policy-001",
                policy_b="policy-002",
            )
        )

        precedence = (
            PolicyPrecedence.resolve(
                higher_priority="policy-002",
                lower_priority="policy-001",
            )
        )

        exception = (
            ExceptionHandling.evaluate(
                policy_id="policy-002",
                exception_requested=False,
            )
        )

        appeal = AppealRecord(
            appeal_id="appeal-001",
            decision_id="decision-001",
            status="OPEN",
        )

        resolution = (
            DisputeResolution.resolve(
                appeal_id="appeal-001",
                resolution="UPHELD",
            )
        )

        state = AdjudicationState(
            adjudication_state="RESOLVED",
        )

        valid = (
            AdjudicationVerifier.verify(
                state
            )
        )

        return {
            "conflict": conflict,
            "precedence": precedence,
            "exception": exception,
            "appeal": appeal.to_dict(),
            "resolution": resolution,
            "state": state.to_dict(),
            "valid": valid,
        }
