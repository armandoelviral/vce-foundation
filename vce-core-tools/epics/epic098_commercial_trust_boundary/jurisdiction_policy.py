from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class JurisdictionPolicy:

    jurisdiction: str
    allowed_regions: List[str]

    def to_dict(self):

        return {
            "jurisdiction": self.jurisdiction,
            "allowed_regions": self.allowed_regions,
        }
