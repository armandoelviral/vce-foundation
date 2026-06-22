from dataclasses import dataclass


@dataclass(frozen=True)
class ConstitutionalState:

    constitutional_state: str

    def to_dict(self):

        return {
            "constitutional_state":
                self.constitutional_state,
        }
