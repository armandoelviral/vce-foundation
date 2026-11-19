"""Deterministic location for one exclusive documentary commitment."""

from dataclasses import dataclass
import hashlib
from pathlib import Path
import struct

from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
)


_DOMAIN = b"PRODUCT001-DOCUMENTARY-LOCATION-V1"


@dataclass(frozen=True, slots=True)
class Product001DocumentaryCommitmentStorageLocation:
    storage_root: Path
    key: Product001DocumentaryCommitmentKey

    def __post_init__(self) -> None:
        if not isinstance(self.storage_root, Path):
            raise TypeError("storage_root must be a Path")
        if not self.storage_root.is_absolute():
            raise ValueError("storage_root must be absolute")
        if self.storage_root.parent == self.storage_root:
            raise ValueError("storage_root must not be filesystem root")
        if not isinstance(
            self.key, Product001DocumentaryCommitmentKey
        ):
            raise TypeError("invalid documentary commitment key")

    @property
    def artifact_path(self) -> Path:
        fields = self.key.exclusive_identity
        encoded = bytearray(_DOMAIN)

        for field in fields:
            value = field.encode("utf-8")
            encoded.extend(struct.pack(">Q", len(value)))
            encoded.extend(value)

        digest = hashlib.sha256(encoded).hexdigest()
        return self.storage_root / f"doc-{digest}.bin"
