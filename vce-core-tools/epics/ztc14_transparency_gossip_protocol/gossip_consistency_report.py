from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class GossipConsistencyReport:

    registry_a: str
    registry_b: str
    consistent: bool

    def to_dict(
        self,
    ) -> Dict[str, Union[str, bool]]:

        return {
            "registry_a": self.registry_a,
            "registry_b": self.registry_b,
            "consistent": self.consistent,
        }
