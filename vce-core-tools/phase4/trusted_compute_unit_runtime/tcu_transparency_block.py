from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TcuTransparencyBlock:

    ledger_index: int
    parent_block_hash: str
    merkle_root: str
    merkle_inclusion_proof: List[str]

    def to_dict(self):

        return {
            "ledger_index": self.ledger_index,
            "parent_block_hash": self.parent_block_hash,
            "merkle_root": self.merkle_root,
            "merkle_inclusion_proof": self.merkle_inclusion_proof,
        }
