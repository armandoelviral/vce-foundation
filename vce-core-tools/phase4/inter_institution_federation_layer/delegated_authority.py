from dataclasses import dataclass


@dataclass(frozen=True)
class DelegatedAuthority:

    source_institution: str
    target_institution: str
    authority: str

    def to_dict(self):

        return {
            "source_institution":
                self.source_institution,
            "target_institution":
                self.target_institution,
            "authority":
                self.authority,
        }
