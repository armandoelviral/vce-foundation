from dataclasses import dataclass


@dataclass(frozen=True)
class ResponseRecoveryRecord:

    citizen_did: str
    recovery_reason: str

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "recovery_reason":
                self.recovery_reason,
            "recorded":
                True,
        }
