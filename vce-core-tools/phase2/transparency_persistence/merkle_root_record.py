from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class MerkleRootRecord:

    root_hash: str
    entry_count: int

    def to_dict(
        self,
    ) -> Dict[str, Union[str, int]]:

        return {
            "root_hash": self.root_hash,
            "entry_count": self.entry_count,
        }
