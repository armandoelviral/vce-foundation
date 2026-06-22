from phase4.constitutional_rights_layer.constitutional_right import (
    ConstitutionalRight,
)

from phase4.constitutional_rights_layer.rights_registry import (
    RightsRegistry,
)

from phase4.constitutional_rights_layer.rights_protection import (
    RightsProtection,
)

from phase4.constitutional_rights_layer.rights_violation import (
    RightsViolation,
)

from phase4.constitutional_rights_layer.rights_appeal import (
    RightsAppeal,
)

from phase4.constitutional_rights_layer.rights_state import (
    RightsState,
)

from phase4.constitutional_rights_layer.rights_verifier import (
    RightsVerifier,
)


class RightsFlow:

    @staticmethod
    def generate():

        right = ConstitutionalRight(
            right_id="right-001",
            right_name="due_process",
        )

        registry = RightsRegistry(
            rights=[right]
        )

        protection = RightsProtection(
            right_id=right.right_id,
            protected=True,
        )

        violation = RightsViolation(
            right_id=right.right_id,
            violation_type="due_process_violation",
        )

        appeal = RightsAppeal(
            appeal_id="rights-appeal-001",
            violation_id="violation-001",
        )

        state = RightsState(
            rights_state="PROTECTED",
        )

        valid = RightsVerifier.verify(
            state
        )

        return {
            "right":
                right.to_dict(),
            "registry":
                registry.to_dict(),
            "protection":
                protection.to_dict(),
            "violation":
                violation.to_dict(),
            "appeal":
                appeal.to_dict(),
            "state":
                state.to_dict(),
            "valid":
                valid,
        }
