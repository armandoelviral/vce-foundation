from dataclasses import dataclass


@dataclass(frozen=True)
class AdmissionDecision:
    admitted: bool
    decision: str
    reason: str

    def to_dict(self):

        return {
            "admitted": self.admitted,
            "decision": self.decision,
            "reason": self.reason,
        }


def admit():

    return AdmissionDecision(
        admitted=True,
        decision="ADMIT",
        reason="ALL_ADMISSION_RULES_SATISFIED",
    )


def reject(
    reason,
):

    return AdmissionDecision(
        admitted=False,
        decision="REJECT",
        reason=reason,
    )
