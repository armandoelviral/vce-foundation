from dataclasses import dataclass


@dataclass(frozen=True)
class ResponseValidation:

    citizen_did: str
    response_valid: bool

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "response_valid":
                self.response_valid,
        }
