from dataclasses import dataclass


@dataclass(frozen=True)
class ResponseValidityState:

    citizen_did: str
    response_state: str

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "response_state":
                self.response_state,
        }
