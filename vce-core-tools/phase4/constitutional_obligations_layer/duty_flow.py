from phase4.constitutional_obligations_layer.constitutional_duty import (
    ConstitutionalDuty,
)

from phase4.constitutional_obligations_layer.duty_registry import (
    DutyRegistry,
)

from phase4.constitutional_obligations_layer.duty_compliance import (
    DutyCompliance,
)

from phase4.constitutional_obligations_layer.duty_violation import (
    DutyViolation,
)

from phase4.constitutional_obligations_layer.duty_appeal import (
    DutyAppeal,
)

from phase4.constitutional_obligations_layer.duty_state import (
    DutyState,
)

from phase4.constitutional_obligations_layer.duty_verifier import (
    DutyVerifier,
)


class DutyFlow:

    @staticmethod
    def generate():

        duty = ConstitutionalDuty(
            duty_id="duty-001",
            duty_name="maintain_response_validity",
        )

        registry = DutyRegistry(
            duties=[duty]
        )

        compliance = DutyCompliance(
            duty_id=duty.duty_id,
            compliant=True,
        )

        violation = DutyViolation(
            duty_id=duty.duty_id,
            violation_type="response_invalidity",
        )

        appeal = DutyAppeal(
            appeal_id="duty-appeal-001",
            violation_id="violation-001",
        )

        state = DutyState(
            duty_state="COMPLIANT",
        )

        valid = DutyVerifier.verify(state)

        return {
            "duty": duty.to_dict(),
            "registry": registry.to_dict(),
            "compliance": compliance.to_dict(),
            "violation": violation.to_dict(),
            "appeal": appeal.to_dict(),
            "state": state.to_dict(),
            "valid": valid,
        }
