"""Tests for documentary storage error taxonomy."""

from sp001.contracts.product001_documentary_commitment_storage_errors import (
    Product001DocumentaryCommitmentStorageError,
    DocumentaryCommitmentConflictError,
    DocumentaryCommitmentStoredArtifactError,
    DocumentaryCommitmentPublicationIndeterminateError,
)


def test_errors_share_storage_base():
    for error_type in (
        DocumentaryCommitmentConflictError,
        DocumentaryCommitmentStoredArtifactError,
        DocumentaryCommitmentPublicationIndeterminateError,
    ):
        assert issubclass(
            error_type,
            Product001DocumentaryCommitmentStorageError,
        )


def test_error_categories_remain_distinct():
    error_types = {
        DocumentaryCommitmentConflictError,
        DocumentaryCommitmentStoredArtifactError,
        DocumentaryCommitmentPublicationIndeterminateError,
    }

    assert len(error_types) == 3


def test_errors_do_not_grant_documentary_authority():
    names = (
        DocumentaryCommitmentConflictError.__name__,
        DocumentaryCommitmentStoredArtifactError.__name__,
        DocumentaryCommitmentPublicationIndeterminateError.__name__,
    )

    assert all("Admission" not in name for name in names)
    assert all("Authorization" not in name for name in names)


def test_storage_io_error_is_distinct():
    from sp001.contracts.product001_documentary_commitment_storage_errors import (
        DocumentaryCommitmentStorageIOError,
    )

    assert issubclass(
        DocumentaryCommitmentStorageIOError,
        Product001DocumentaryCommitmentStorageError,
    )

    assert not issubclass(
        DocumentaryCommitmentStorageIOError,
        DocumentaryCommitmentConflictError,
    )

    assert not issubclass(
        DocumentaryCommitmentStorageIOError,
        DocumentaryCommitmentPublicationIndeterminateError,
    )
