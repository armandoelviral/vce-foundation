from dataclasses import dataclass
from enum import StrEnum
import os
from pathlib import Path
import stat

from sp001.contracts.evidence_file_expectation import EvidenceFileExpectation
from sp001.contracts.knowledge_source_identity import KnowledgeContentDigest
from sp001.services.knowledge_source_integrity import digest_knowledge_source_content


class EvidenceFileComparisonStatus(StrEnum):
    MATCH = "MATCH"
    DIFFERENT = "DIFFERENT"
    NOT_FOUND = "NOT_FOUND"
    LIMIT_EXCEEDED = "LIMIT_EXCEEDED"
    CHANGED_DURING_READ = "CHANGED_DURING_READ"


@dataclass(frozen=True, slots=True)
class EvidenceFileComparison:
    """Local byte observation; no authenticity, approval or future-path guarantee."""

    expectation: EvidenceFileExpectation
    status: EvidenceFileComparisonStatus
    observed_byte_length: int | None
    observed_digest: KnowledgeContentDigest | None


def _metadata(value):
    return (
        value.st_dev, value.st_ino, value.st_size,
        value.st_mtime_ns, value.st_ctime_ns,
    )


def compare_evidence_file(
    *, expectation: EvidenceFileExpectation, path: Path, max_bytes: int,
) -> EvidenceFileComparison:
    """Compare bytes from one opened regular file within an explicit size limit.

    Paths are supplied by a trusted local caller; this is not a path sandbox.
    Changed metadata prevents a conclusive result, but cannot prove an atomic
    filesystem snapshot against concurrent writers.
    """
    if type(expectation) is not EvidenceFileExpectation:
        raise TypeError("expectation must be an EvidenceFileExpectation")
    if not isinstance(path, Path):
        raise TypeError("path must be a Path")
    if type(max_bytes) is not int:
        raise TypeError("max_bytes must be an integer")
    if max_bytes < 1:
        raise ValueError("max_bytes must be positive")

    def result(status, length=None, digest=None):
        return EvidenceFileComparison(expectation, status, length, digest)

    if expectation.byte_length > max_bytes:
        raise ValueError("expected content exceeds configured read limit")

    # Nonblocking open avoids waiting on a FIFO before checking file type.
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    try:
        descriptor = os.open(path, flags)
    except FileNotFoundError:
        return result(EvidenceFileComparisonStatus.NOT_FOUND)

    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError("evidence path must identify a regular file")
        if before.st_size > max_bytes:
            return result(EvidenceFileComparisonStatus.LIMIT_EXCEEDED)

        # fdopen owns a duplicate; the original descriptor always closes below.
        with os.fdopen(os.dup(descriptor), "rb") as stream:
            content = stream.read(max_bytes + 1)
        after = os.fstat(descriptor)
        if len(content) > max_bytes:
            return result(EvidenceFileComparisonStatus.LIMIT_EXCEEDED)
        if (
            _metadata(before) != _metadata(after)
            or len(content) != after.st_size
        ):
            return result(EvidenceFileComparisonStatus.CHANGED_DURING_READ)

        # Existing source hashing deliberately rejects empty content.
        digest = (
            digest_knowledge_source_content(content=content) if content else None
        )
        matches = (
            len(content) == expectation.byte_length
            and digest == expectation.identity.source_content_digest
        )
        return result(
            EvidenceFileComparisonStatus.MATCH if matches
            else EvidenceFileComparisonStatus.DIFFERENT,
            len(content), digest,
        )
    finally:
        os.close(descriptor)
