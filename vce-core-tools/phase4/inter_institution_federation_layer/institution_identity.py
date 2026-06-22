from dataclasses import dataclass


@dataclass(frozen=True)
class InstitutionIdentity:

    institution_id: str
    institution_name: str

    def to_dict(self):

        return {
            "institution_id": self.institution_id,
            "institution_name": self.institution_name,
        }
