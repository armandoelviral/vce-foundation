from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SP1SDKConfig:

    sdk_path: str
    elf_path: str
    prover_mode: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "sdk_path": self.sdk_path,
            "elf_path": self.elf_path,
            "prover_mode": self.prover_mode,
        }
