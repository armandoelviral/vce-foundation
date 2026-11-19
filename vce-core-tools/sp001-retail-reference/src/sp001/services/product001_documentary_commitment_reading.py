"""Validated local reading of exclusive documentary commitments."""

import errno
import os
import stat

from sp001.contracts.product001_documentary_commitment_reading import (
    Product001DocumentaryCommitmentReadResult,
    Product001DocumentaryCommitmentReadStatus as Status,
)
from sp001.contracts.product001_documentary_commitment_storage_location import (
    Product001DocumentaryCommitmentStorageLocation,
)
from sp001.services.product001_documentary_commitment_serialization import (
    InvalidDocumentaryCommitmentArtifactError,
    deserialize_product001_documentary_commitment,
)


def read_product001_documentary_commitment(
    *,
    location: Product001DocumentaryCommitmentStorageLocation,
) -> Product001DocumentaryCommitmentReadResult:
    """Read a local artifact without granting documentary admission."""

    if not isinstance(
        location, Product001DocumentaryCommitmentStorageLocation
    ):
        raise TypeError("invalid documentary storage location")

    def result(status, content=None):
        return Product001DocumentaryCommitmentReadResult(
            key=location.key,
            status=status,
            content=content,
        )

    root = location.storage_root

    try:
        root_stat = root.lstat()
    except OSError:
        return result(Status.IO_FAILURE)

    if not stat.S_ISDIR(root_stat.st_mode):
        return result(Status.IO_FAILURE)

    root_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW

    try:
        root_descriptor = os.open(root, root_flags)
    except OSError:
        return result(Status.IO_FAILURE)

    descriptor = None
    opening_status = None

    try:
        opened_root = os.fstat(root_descriptor)

        if (
            not stat.S_ISDIR(opened_root.st_mode)
            or (
                opened_root.st_dev,
                opened_root.st_ino,
            ) != (
                root_stat.st_dev,
                root_stat.st_ino,
            )
        ):
            opening_status = Status.IO_FAILURE
        else:
            flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK

            try:
                descriptor = os.open(
                    location.artifact_path.name,
                    flags,
                    dir_fd=root_descriptor,
                )
            except FileNotFoundError:
                opening_status = Status.ABSENT
            except OSError as error:
                if error.errno in (errno.ELOOP, errno.EISDIR):
                    opening_status = Status.INVALID
                else:
                    opening_status = Status.IO_FAILURE

    except OSError:
        opening_status = Status.IO_FAILURE

    try:
        os.close(root_descriptor)
    except OSError:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass
        return result(Status.IO_FAILURE)

    if opening_status is Status.ABSENT:
        try:
            current_root = root.lstat()
        except OSError:
            return result(Status.IO_FAILURE)

        if (
            not stat.S_ISDIR(current_root.st_mode)
            or (
                current_root.st_dev,
                current_root.st_ino,
            ) != (
                opened_root.st_dev,
                opened_root.st_ino,
            )
        ):
            return result(Status.IO_FAILURE)

        return result(Status.ABSENT)

    if opening_status is not None:
        return result(opening_status)

    artifact = None
    read_status = None

    close_failed = False

    try:
        try:
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                read_status = Status.INVALID
            else:
                with os.fdopen(descriptor, "rb", closefd=False) as stream:
                    artifact = stream.read()
        except OSError:
            read_status = Status.IO_FAILURE
    finally:
        try:
            os.close(descriptor)
        except OSError:
            close_failed = True

    if close_failed:
        return result(Status.IO_FAILURE)

    if read_status is not None:
        return result(read_status)

    try:
        stored_key, content = (
            deserialize_product001_documentary_commitment(artifact)
        )
    except (InvalidDocumentaryCommitmentArtifactError, TypeError):
        return result(Status.INVALID)

    if stored_key.exclusive_identity != location.key.exclusive_identity:
        return result(Status.INVALID)

    if (
        stored_key.source_identity.source_content_digest
        != location.key.source_identity.source_content_digest
    ):
        return result(Status.CONFLICT)

    return result(Status.PRESENT, content)
