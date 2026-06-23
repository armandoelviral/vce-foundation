from dataclasses import dataclass
from typing import List

from phase4.constitutional_economy_layer.capital_record import (
    CapitalRecord,
)


@dataclass(frozen=True)
class CapitalRegistry:

    records: List[CapitalRecord]

    def to_dict(self):

        return {
            "records": [
                record.to_dict()
                for record in self.records
            ]
        }
