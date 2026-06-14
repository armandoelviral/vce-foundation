from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class GossipMessage:
    registry_id: str
    transparency_root: str
    sequence_number: int

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            "registry_id": self.registry_id,
            "transparency_root": self.transparency_root,
            "sequence_number": self.sequence_number,
        }
