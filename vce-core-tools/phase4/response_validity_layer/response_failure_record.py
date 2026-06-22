from dataclasses import dataclass


@dataclass(frozen=True)
class ResponseFailureRecord:

    citizen_did: str
    failure_reason: str

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "failure_reason":
                self.failure_reason,
            "recorded":
                True,
        }
