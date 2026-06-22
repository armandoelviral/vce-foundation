from dataclasses import dataclass


@dataclass(frozen=True)
class InterInstitutionTrust:

    source_institution: str
    target_institution: str
    trusted: bool

    def to_dict(self):

        return {
            "source_institution":
                self.source_institution,
            "target_institution":
                self.target_institution,
            "trusted":
                self.trusted,
        }
