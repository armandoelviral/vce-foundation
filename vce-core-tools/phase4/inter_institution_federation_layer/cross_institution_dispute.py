from dataclasses import dataclass


@dataclass(frozen=True)
class CrossInstitutionDispute:

    dispute_id: str
    institution_a: str
    institution_b: str
    treaty_id: str

    def to_dict(self):

        return {
            "dispute_id":
                self.dispute_id,
            "institution_a":
                self.institution_a,
            "institution_b":
                self.institution_b,
            "treaty_id":
                self.treaty_id,
        }
