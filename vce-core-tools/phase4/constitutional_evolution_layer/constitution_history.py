from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ConstitutionHistory:

    versions: List[str]

    def latest_version(self):

        return self.versions[-1]

    def to_dict(self):

        return {
            "versions": self.versions,
            "latest_version":
                self.latest_version(),
        }
