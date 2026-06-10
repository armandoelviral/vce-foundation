from dataclasses import dataclass


@dataclass(frozen=True)
class CRRReplicationPolicy:
    source_bucket: str
    destination_bucket: str
    source_region: str
    destination_region: str
    object_lock_replication: bool
    versioning_required: bool
    enabled: bool

    def is_valid(self):

        return (
            self.enabled is True
            and self.versioning_required is True
            and self.object_lock_replication is True
            and self.source_region != self.destination_region
        )
