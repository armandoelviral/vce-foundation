"""Errors for exclusive documentary commitment storage."""


class Product001DocumentaryCommitmentStorageError(Exception):
    """Base error for documentary storage operations."""


class DocumentaryCommitmentConflictError(
    Product001DocumentaryCommitmentStorageError
):
    """An exclusive identity already contains different content."""


class DocumentaryCommitmentStoredArtifactError(
    Product001DocumentaryCommitmentStorageError
):
    """An existing documentary artifact cannot be validated."""


class DocumentaryCommitmentPublicationIndeterminateError(
    Product001DocumentaryCommitmentStorageError
):
    """Publication may have occurred without confirmed durability."""



class DocumentaryCommitmentStorageIOError(
    Product001DocumentaryCommitmentStorageError
):
    """Storage I/O failed without confirmed publication."""
