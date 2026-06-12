from dataclasses import dataclass


@dataclass(frozen=True)
class AnchorReceipt:
    root_hash: str
    target_id: str
    target_type: str
    anchor_reference: str
    anchored_at: str
    status: str

    def to_dict(self):

        return {
            "root_hash": self.root_hash,
            "target_id": self.target_id,
            "target_type": self.target_type,
            "anchor_reference": self.anchor_reference,
            "anchored_at": self.anchored_at,
            "status": self.status,
        }
