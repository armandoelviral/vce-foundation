from dataclasses import dataclass


@dataclass(frozen=True)
class TreatyRecord:

    treaty_id: str
    institution_a: str
    institution_b: str
    treaty_type: str

    def to_dict(self):

        return {
            "treaty_id":
                self.treaty_id,
            "institution_a":
                self.institution_a,
            "institution_b":
                self.institution_b,
            "treaty_type":
                self.treaty_type,
        }
