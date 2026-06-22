from dataclasses import dataclass
from typing import List

from phase4.constitutional_identity_layer.identity_right import (
    IdentityRight,
)


@dataclass(frozen=True)
class IdentityRegistry:

    identities: List[IdentityRight]

    def to_dict(self):

        return {
            "identities": [
                identity.to_dict()
                for identity in self.identities
            ]
        }
