from dataclasses import dataclass
from typing import List

from phase4.inter_institution_federation_layer.institution_identity import (
    InstitutionIdentity,
)


@dataclass(frozen=True)
class InstitutionRegistry:

    institutions: List[InstitutionIdentity]

    def to_dict(self):

        return {
            "institutions": [
                institution.to_dict()
                for institution in self.institutions
            ]
        }
