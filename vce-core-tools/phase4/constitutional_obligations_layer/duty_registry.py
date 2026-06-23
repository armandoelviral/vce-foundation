from dataclasses import dataclass
from typing import List

from phase4.constitutional_obligations_layer.constitutional_duty import (
    ConstitutionalDuty,
)


@dataclass(frozen=True)
class DutyRegistry:

    duties: List[ConstitutionalDuty]

    def to_dict(self):

        return {
            "duties": [
                duty.to_dict()
                for duty in self.duties
            ]
        }
