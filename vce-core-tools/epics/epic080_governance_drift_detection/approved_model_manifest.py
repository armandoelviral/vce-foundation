from dataclasses import dataclass


@dataclass(frozen=True)
class ApprovedModelManifest:
    model_id: str
    model_version: str
    model_hash: str
    weights_hash: str
    runtime_image_hash: str
    approved_by: str
    approved_at: str

    def to_dict(self):

        return {
            "model_id": self.model_id,
            "model_version": self.model_version,
            "model_hash": self.model_hash,
            "weights_hash": self.weights_hash,
            "runtime_image_hash": self.runtime_image_hash,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
        }
