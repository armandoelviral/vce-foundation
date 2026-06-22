from dataclasses import dataclass


@dataclass(frozen=True)
class ResponseCapability:

    citizen_did: str
    response_capable: bool

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "response_capable":
                self.response_capable,
        }
