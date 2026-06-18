from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class ReplayComparatorResult:

    expected_hash: str
    actual_hash: str
    match: bool

    def to_dict(
        self,
    ) -> Dict[str, Union[str, bool]]:

        return {
            "expected_hash": self.expected_hash,
            "actual_hash": self.actual_hash,
            "match": self.match,
        }
