"""Fail-closed documentary verification for commercial decisions.

A successful read is a point-in-time integrity observation,
not documentary admission or commercial authorization.
"""

import hashlib
from pathlib import Path

from sp001.contracts.product001_commercial_approval_decision import (
    Product001CommercialApprovalDecision,
)
from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
)
from sp001.contracts.product001_documentary_commitment_reading import (
    Product001DocumentaryCommitmentReadResult,
    Product001DocumentaryCommitmentReadStatus,
)
from sp001.contracts.product001_documentary_commitment_storage_location import (
    Product001DocumentaryCommitmentStorageLocation,
)
from sp001.services.product001_documentary_commitment_reading import (
    read_product001_documentary_commitment,
)


class CommercialDocumentVerificationRejected(PermissionError):
    def __init__(self, status: str):
        self.status = status
        super().__init__(f"commercial document rejected: {status}")


class Product001CommercialDocumentVerifier:
    def __init__(self, *, storage_root: Path, reader=None):
        if not isinstance(storage_root, Path):
            raise TypeError("storage_root must be a Path")
        if not storage_root.is_absolute():
            raise ValueError("storage_root must be absolute")
        if storage_root.parent == storage_root:
            raise ValueError("storage_root must not be filesystem root")

        if reader is None:
            reader = read_product001_documentary_commitment
        if not callable(reader):
            raise TypeError("reader must be callable")

        self._storage_root = storage_root
        self._reader = reader

    def verify(self, *, decision: Product001CommercialApprovalDecision) -> None:
        if not isinstance(decision, Product001CommercialApprovalDecision):
            raise TypeError("invalid commercial decision")

        key = Product001DocumentaryCommitmentKey(
            organization_id=decision.document_scope.organization_id,
            source_identity=decision.document_identity,
        )
        location = Product001DocumentaryCommitmentStorageLocation(
            storage_root=self._storage_root,
            key=key,
        )

        result = self._reader(location=location)

        if not isinstance(result, Product001DocumentaryCommitmentReadResult):
            raise CommercialDocumentVerificationRejected(
                "INVALID_READER_RESULT"
            )

        if result.key != key:
            raise CommercialDocumentVerificationRejected(
                "IDENTITY_MISMATCH"
            )

        if result.status is not Product001DocumentaryCommitmentReadStatus.PRESENT:
            raise CommercialDocumentVerificationRejected(
                result.status.value
            )

        if hashlib.sha256(result.content).hexdigest() != (
            key.source_identity.source_content_digest.value
        ):
            raise CommercialDocumentVerificationRejected(
                "CONTENT_DIGEST_MISMATCH"
            )
