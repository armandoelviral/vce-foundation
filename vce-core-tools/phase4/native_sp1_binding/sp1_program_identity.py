from dataclasses import dataclass


@dataclass(frozen=True)
class SP1ProgramIdentity:

    tcu_did: str
    program_id: str
    program_hash: str

    def to_dict(self):

        return {
            "tcu_did": self.tcu_did,
            "program_id": self.program_id,
            "program_hash": self.program_hash,
        }
