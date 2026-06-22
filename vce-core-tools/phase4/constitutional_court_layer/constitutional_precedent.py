from dataclasses import dataclass


@dataclass(frozen=True)
class ConstitutionalPrecedent:

    case_id: str
    precedent: str

    def to_dict(self):

        return {
            "case_id":
                self.case_id,
            "precedent":
                self.precedent,
        }
