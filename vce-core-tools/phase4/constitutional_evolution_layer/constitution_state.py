from dataclasses import dataclass


@dataclass(frozen=True)
class ConstitutionState:

    constitution_state: str

    def to_dict(self):

        return {
            "constitution_state":
                self.constitution_state,
        }
