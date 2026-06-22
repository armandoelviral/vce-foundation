from dataclasses import dataclass


@dataclass(frozen=True)
class RightsState:

    citizen_did: str
    rights_state: str

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "rights_state":
                self.rights_state,
        }
