from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class VcrDidRecord:

    did: str
    controller: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "did":
                self.did,

            "controller":
                self.controller,
        }
