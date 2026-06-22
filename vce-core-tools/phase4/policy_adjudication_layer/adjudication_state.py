from dataclasses import dataclass


@dataclass(frozen=True)
class AdjudicationState:

    adjudication_state: str

    def to_dict(self):

        return {
            "adjudication_state":
                self.adjudication_state,
        }
