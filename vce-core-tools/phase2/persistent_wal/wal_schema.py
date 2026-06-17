from dataclasses import dataclass


@dataclass(frozen=True)
class WALRecord:

    lsn: int
    opcode: str
    payload: dict

    previous_hash: str
    current_hash: str

    def to_dict(
        self,
    ) -> dict:

        return {
            "lsn": self.lsn,
            "opcode": self.opcode,
            "payload": self.payload,
            "previous_hash": self.previous_hash,
            "current_hash": self.current_hash,
        }
