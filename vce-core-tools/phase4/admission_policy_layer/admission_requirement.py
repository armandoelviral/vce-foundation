from dataclasses import dataclass


@dataclass(frozen=True)
class AdmissionRequirement:

    requirement_name: str
    requirement_value: int

    def to_dict(self):

        return {
            "requirement_name":
                self.requirement_name,
            "requirement_value":
                self.requirement_value,
        }
