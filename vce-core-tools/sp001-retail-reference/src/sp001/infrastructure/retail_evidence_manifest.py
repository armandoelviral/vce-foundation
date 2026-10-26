import json
import os
from pathlib import Path
import stat

from sp001.contracts.evidence_file_expectation import EvidenceFileExpectation
from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest, KnowledgeSourceIdentity,
)
from sp001.infrastructure.evidence_file_comparison import compare_evidence_file
from sp001.services.retail_report_evidence_comparison import (
    bind_retail_report_evidence_comparisons,
)


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate manifest key")
        result[key] = value
    return result


def _invalid_number(value):
    raise ValueError("unsupported manifest number")


def _read_manifest(path, limit):
    descriptor = os.open(
        path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0),
    )
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError("manifest must be a regular file")
        if metadata.st_size > limit:
            raise ValueError("manifest exceeds read limit")
        with os.fdopen(os.dup(descriptor), "rb") as stream:
            content = stream.read(limit + 1)
        if len(content) > limit:
            raise ValueError("manifest exceeds read limit")
        return content
    finally:
        os.close(descriptor)


def compare_retail_evidence_manifest(
    *, report, manifest_path: Path,
    max_manifest_bytes: int, max_evidence_bytes: int,
):
    """Read operator-supplied paths; caller must authorize report access first."""
    if not isinstance(manifest_path, Path):
        raise TypeError("manifest_path must be a Path")
    for limit in (max_manifest_bytes, max_evidence_bytes):
        if type(limit) is not int or limit < 1:
            raise ValueError("read limits must be positive integers")

    document = json.loads(
        _read_manifest(manifest_path, max_manifest_bytes).decode("utf-8"),
        object_pairs_hook=_unique,
        parse_float=_invalid_number, parse_constant=_invalid_number,
    )
    if type(document) is not dict or set(document) != {"schema_version", "evidence"}:
        raise ValueError("invalid manifest envelope")
    if type(document["schema_version"]) is not int or document["schema_version"] != 1:
        raise ValueError("unsupported manifest version")
    if type(document["evidence"]) is not list:
        raise ValueError("evidence must be a list")

    entries = []
    for raw in document["evidence"]:
        if type(raw) is not dict or set(raw) != {
            "evidence_id", "version", "byte_length", "sha256", "path",
        }:
            raise ValueError("invalid evidence entry")
        if type(raw["path"]) is not str or not raw["path"].strip():
            raise ValueError("evidence path must be nonempty text")
        expected = EvidenceFileExpectation(
            KnowledgeSourceIdentity(
                raw["evidence_id"], raw["version"],
                KnowledgeContentDigest("SHA-256", raw["sha256"]),
            ),
            raw["byte_length"],
        )
        if expected.byte_length > max_evidence_bytes:
            raise ValueError("expected evidence exceeds read limit")
        path = Path(raw["path"])
        if not path.is_absolute():
            path = manifest_path.parent / path
        entries.append((expected, path))

    expectations = tuple(expected for expected, _ in entries)
    # Reject foreign or ambiguous identities before opening evidence files.
    bind_retail_report_evidence_comparisons(
        report=report, expectations=expectations, comparisons=(),
    )
    comparisons = tuple(
        compare_evidence_file(
            expectation=expected, path=path, max_bytes=max_evidence_bytes,
        )
        for expected, path in entries
    )
    return bind_retail_report_evidence_comparisons(
        report=report, expectations=expectations, comparisons=comparisons,
    )
