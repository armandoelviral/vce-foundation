from dataclasses import dataclass
from typing import List

from phase4.constitutional_rights_layer.constitutional_right import (
    ConstitutionalRight,
)


@dataclass(frozen=True)
class RightsRegistry:

    rights: List[ConstitutionalRight]

    def to_dict(self):

        return {
            "rights": [
                right.to_dict()
                for right in self.rights
            ]
        }
