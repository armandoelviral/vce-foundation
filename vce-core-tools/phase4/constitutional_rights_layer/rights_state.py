from dataclasses import dataclass


@dataclass(frozen=True)
class RightsState:

    rights_state: str

    def to_dict(self):

        return {
            "rights_state": self.rights_state,
        }
