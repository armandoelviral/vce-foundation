from dataclasses import dataclass


@dataclass(frozen=True)
class ConstitutionVersion:

    version: str

    def to_dict(self):

        return {
            "version":
                self.version,
        }
