from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationRecovery:

    citizen_did: str
    recovery_reason: str
    recovery_points: int

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "recovery_reason":
                self.recovery_reason,
            "recovery_points":
                self.recovery_points,
        }
