"""Exclusive local publication of documentary commitments."""

import errno
import os
import stat
import tempfile
import sys
from pathlib import Path

from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentResult,
    Product001DocumentaryCommitmentStatus,
)
from sp001.contracts.product001_documentary_commitment_storage_errors import (
    DocumentaryCommitmentConflictError,
    DocumentaryCommitmentStoredArtifactError,
    DocumentaryCommitmentPublicationIndeterminateError,
    DocumentaryCommitmentStorageIOError,
)
from sp001.contracts.product001_documentary_commitment_storage_location import (
    Product001DocumentaryCommitmentStorageLocation,
)
from sp001.services.product001_documentary_commitment_serialization import (
    InvalidDocumentaryCommitmentArtifactError,
    deserialize_product001_documentary_commitment,
    serialize_product001_documentary_commitment,
)


def _fsync_directory(directory: Path) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY

    descriptor = os.open(directory, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _read_existing(
    location: Product001DocumentaryCommitmentStorageLocation,
) -> bytes:
    path = location.artifact_path

    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW

    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        if isinstance(error, OSError) and error.errno == errno.ELOOP:
            raise DocumentaryCommitmentStoredArtifactError(
                "existing artifact is a symbolic link"
            ) from error
        raise DocumentaryCommitmentStorageIOError(
            "existing artifact cannot be opened"
        ) from error

    try:
        with os.fdopen(descriptor, "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise DocumentaryCommitmentStoredArtifactError(
                    "existing artifact is not a regular file"
                )
            artifact = stream.read()
    except OSError as error:
        raise DocumentaryCommitmentStorageIOError(
            "existing artifact cannot be read"
        ) from error

    try:
        stored_key, stored_content = (
            deserialize_product001_documentary_commitment(artifact)
        )
    except (InvalidDocumentaryCommitmentArtifactError, TypeError) as error:
        raise DocumentaryCommitmentStoredArtifactError(
            "existing documentary artifact is invalid"
        ) from error

    if stored_key.exclusive_identity != location.key.exclusive_identity:
        raise DocumentaryCommitmentStoredArtifactError(
            "stored documentary identity does not match location"
        )

    return stored_content


def write_product001_documentary_commitment(
    *,
    location: Product001DocumentaryCommitmentStorageLocation,
    content: bytes,
) -> Product001DocumentaryCommitmentResult:
    if not isinstance(
        location, Product001DocumentaryCommitmentStorageLocation
    ):
        raise TypeError("invalid documentary storage location")

    artifact = serialize_product001_documentary_commitment(
        key=location.key,
        content=content,
    )

    root = location.storage_root
    destination = location.artifact_path

    if not root.is_dir() or root.is_symlink():
        raise ValueError(
            "storage_root must be an existing real directory"
        )

    temporary_path = None
    published = False

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=".product001-",
            suffix=".tmp",
            dir=root,
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(artifact)
            temporary.flush()
            os.fsync(temporary.fileno())

        try:
            os.link(temporary_path, destination)
        except FileExistsError:
            existing_content = _read_existing(location)

            if existing_content != content:
                raise DocumentaryCommitmentConflictError(
                    "exclusive documentary identity already exists "
                    "with different content"
                )

            return Product001DocumentaryCommitmentResult(
                key=location.key,
                status=Product001DocumentaryCommitmentStatus.ALREADY_PRESENT,
                bytes_committed=len(content),
            )
        except OSError as error:
            raise DocumentaryCommitmentPublicationIndeterminateError(
                "exclusive documentary publication outcome is unconfirmed"
            ) from error

        published = True

        try:
            _fsync_directory(root)
        except OSError as error:
            raise DocumentaryCommitmentPublicationIndeterminateError(
                "documentary publication durability is unconfirmed"
            ) from error

        return Product001DocumentaryCommitmentResult(
            key=location.key,
            status=Product001DocumentaryCommitmentStatus.CREATED,
            bytes_committed=len(content),
        )

    except OSError as error:
        raise DocumentaryCommitmentStorageIOError(
            "documentary temporary storage operation failed"
        ) from error
    finally:
        if temporary_path is not None:
            primary_error = sys.exception()
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError as cleanup_error:
                if primary_error is not None:
                    primary_error.add_note(
                        "documentary temporary cleanup failed: "
                        f"{type(cleanup_error).__name__}"
                    )
                elif published:
                    raise DocumentaryCommitmentPublicationIndeterminateError(
                        "documentary artifact was published, "
                        "but temporary cleanup failed"
                    ) from cleanup_error
                else:
                    raise DocumentaryCommitmentStorageIOError(
                        "documentary temporary cleanup failed"
                    ) from cleanup_error
