import os
from pathlib import Path

import pytest

from sp001.contracts.evidence_file_expectation import EvidenceFileExpectation
from sp001.contracts.knowledge_source_identity import KnowledgeSourceIdentity
from sp001.infrastructure import evidence_file_comparison as module
from sp001.infrastructure.evidence_file_comparison import (
    compare_evidence_file, EvidenceFileComparisonStatus as Status,
)
from sp001.services.knowledge_source_integrity import digest_knowledge_source_content


def expectation(content=b"original"):
    return EvidenceFileExpectation(
        KnowledgeSourceIdentity(
            "EVIDENCE-1", "1",
            digest_knowledge_source_content(content=content),
        ),
        len(content),
    )


def test_matches_exact_binary_content_without_rewriting_file(tmp_path):
    content = b"\x00\xfforiginal\r\n"
    path = tmp_path / "evidence.bin"
    path.write_bytes(content)
    expected = expectation(content)
    result = compare_evidence_file(
        expectation=expected, path=path, max_bytes=100,
    )
    assert result.status is Status.MATCH
    assert result.expectation is expected
    assert result.observed_byte_length == len(content)
    assert result.observed_digest == expected.identity.source_content_digest
    assert path.read_bytes() == content


@pytest.mark.parametrize("content", [b"modified", b"short", b""])
def test_changed_or_empty_content_is_different(tmp_path, content):
    path = tmp_path / "evidence.bin"
    path.write_bytes(content)
    result = compare_evidence_file(
        expectation=expectation(), path=path, max_bytes=100,
    )
    assert result.status is Status.DIFFERENT
    assert result.observed_byte_length == len(content)
    assert (result.observed_digest is None) == (content == b"")


def test_missing_file_is_explicit_and_creates_nothing(tmp_path):
    path = tmp_path / "absent" / "evidence.bin"
    result = compare_evidence_file(
        expectation=expectation(), path=path, max_bytes=100,
    )
    assert result.status is Status.NOT_FOUND
    assert result.observed_digest is None
    assert result.observed_byte_length is None
    assert not path.parent.exists()


def test_oversized_file_does_not_produce_a_partial_digest(tmp_path):
    path = tmp_path / "large.bin"
    path.write_bytes(b"x" * 101)
    result = compare_evidence_file(
        expectation=expectation(), path=path, max_bytes=100,
    )
    assert result.status is Status.LIMIT_EXCEEDED
    assert result.observed_digest is None
    assert result.observed_byte_length is None


def test_permission_error_is_not_absence(tmp_path, monkeypatch):
    failure = PermissionError("synthetic access failure")

    def denied(*args, **kwargs):
        raise failure

    monkeypatch.setattr(module.os, "open", denied)
    with pytest.raises(PermissionError) as caught:
        compare_evidence_file(
            expectation=expectation(), path=tmp_path / "file", max_bytes=100,
        )
    assert caught.value is failure


def test_metadata_change_prevents_conclusive_comparison(tmp_path, monkeypatch):
    path = tmp_path / "file"
    path.write_bytes(b"original")
    original_fstat = os.fstat
    calls = []

    def changed(descriptor):
        calls.append(True)
        if len(calls) == 2:
            path.write_bytes(b"modified")
        return original_fstat(descriptor)

    monkeypatch.setattr(module.os, "fstat", changed)
    result = compare_evidence_file(
        expectation=expectation(), path=path, max_bytes=100,
    )
    assert result.status is Status.CHANGED_DURING_READ
    assert result.observed_digest is None


def test_directory_is_not_absent_or_different_content(tmp_path):
    with pytest.raises((ValueError, IsADirectoryError)):
        compare_evidence_file(
            expectation=expectation(), path=tmp_path, max_bytes=100,
        )


@pytest.mark.parametrize("limit,error", [(True, TypeError), (0, ValueError)])
def test_rejects_invalid_limits(tmp_path, limit, error):
    with pytest.raises(error):
        compare_evidence_file(
            expectation=expectation(), path=tmp_path / "file", max_bytes=limit,
        )


def test_expected_size_must_fit_read_budget(tmp_path):
    with pytest.raises(ValueError, match="exceeds"):
        compare_evidence_file(
            expectation=expectation(), path=tmp_path / "file", max_bytes=1,
        )


def test_expectation_rejects_empty_size_and_bool():
    identity = expectation().identity
    with pytest.raises(ValueError):
        EvidenceFileExpectation(identity, 0)
    with pytest.raises(TypeError):
        EvidenceFileExpectation(identity, True)
