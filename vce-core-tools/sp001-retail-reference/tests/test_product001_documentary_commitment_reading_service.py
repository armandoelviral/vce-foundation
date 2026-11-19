"""Behavioral tests for local documentary commitment reading."""

import hashlib
import os

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
)
from sp001.contracts.product001_documentary_commitment_reading import (
    Product001DocumentaryCommitmentReadStatus as Status,
)
from sp001.contracts.product001_documentary_commitment_storage_location import (
    Product001DocumentaryCommitmentStorageLocation,
)
from sp001.services.product001_documentary_commitment_reading import (
    read_product001_documentary_commitment,
)
from sp001.services.product001_documentary_commitment_serialization import (
    serialize_product001_documentary_commitment,
)


def make_location(root, content=b"document"):
    key = Product001DocumentaryCommitmentKey(
        organization_id="org-1",
        source_identity=KnowledgeSourceIdentity(
            source_id="planogram-1",
            source_version="v1",
            source_content_digest=KnowledgeContentDigest(
                algorithm="SHA-256",
                value=hashlib.sha256(content).hexdigest(),
            ),
        ),
    )
    return Product001DocumentaryCommitmentStorageLocation(
        storage_root=root,
        key=key,
    )


def read(location):
    return read_product001_documentary_commitment(location=location)


def test_absent(tmp_path):
    location = make_location(tmp_path)
    assert read(location).status is Status.ABSENT


def test_present(tmp_path):
    content = b"document"
    location = make_location(tmp_path, content)
    location.artifact_path.write_bytes(
        serialize_product001_documentary_commitment(
            key=location.key, content=content
        )
    )
    result = read(location)
    assert result.status is Status.PRESENT
    assert result.content == content


def test_conflict(tmp_path):
    stored = make_location(tmp_path, b"original")
    requested = make_location(tmp_path, b"changed")
    assert stored.artifact_path == requested.artifact_path

    stored.artifact_path.write_bytes(
        serialize_product001_documentary_commitment(
            key=stored.key, content=b"original"
        )
    )
    result = read(requested)
    assert result.status is Status.CONFLICT
    assert result.content is None


def test_invalid_artifact(tmp_path):
    location = make_location(tmp_path)
    location.artifact_path.write_bytes(b"corrupt")
    assert read(location).status is Status.INVALID


def test_invalid_exclusive_identity(tmp_path):
    location = make_location(tmp_path)
    other_key = Product001DocumentaryCommitmentKey(
        organization_id="other-org",
        source_identity=location.key.source_identity,
    )
    location.artifact_path.write_bytes(
        serialize_product001_documentary_commitment(
            key=other_key, content=b"document"
        )
    )
    assert read(location).status is Status.INVALID


def test_symlink_destination(tmp_path):
    location = make_location(tmp_path)
    target = tmp_path / "target"
    target.write_bytes(b"document")
    location.artifact_path.symlink_to(target)
    assert read(location).status is Status.INVALID


def test_directory_destination(tmp_path):
    location = make_location(tmp_path)
    location.artifact_path.mkdir()
    assert read(location).status is Status.INVALID


def test_missing_root_is_io_failure(tmp_path):
    location = make_location(tmp_path / "missing")
    assert read(location).status is Status.IO_FAILURE


def test_root_symlink_is_io_failure(tmp_path):
    actual = tmp_path / "actual"
    actual.mkdir()
    alias = tmp_path / "alias"
    alias.symlink_to(actual, target_is_directory=True)
    assert read(make_location(alias)).status is Status.IO_FAILURE


def test_open_error_is_io_failure(tmp_path, monkeypatch):
    location = make_location(tmp_path)

    def fail_open(*args, **kwargs):
        raise PermissionError(errno_value, "denied")

    errno_value = 13
    monkeypatch.setattr(os, "open", fail_open)
    assert read(location).status is Status.IO_FAILURE


def test_read_does_not_create_artifact(tmp_path):
    location = make_location(tmp_path)
    before = set(tmp_path.iterdir())
    assert read(location).status is Status.ABSENT
    assert set(tmp_path.iterdir()) == before


def test_rejects_invalid_location():
    with pytest.raises(TypeError):
        read_product001_documentary_commitment(location="invalid")


def test_root_disappears_during_open_is_not_absent(
    tmp_path, monkeypatch
):
    root = tmp_path / "storage"
    root.mkdir()
    location = make_location(root)

    original_open = os.open

    def disappear_before_open(path, flags, *args, **kwargs):
        root.rmdir()
        return original_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(os, "open", disappear_before_open)

    result = read(location)

    assert result.status is Status.IO_FAILURE


def test_fstat_failure_is_io_failure(tmp_path, monkeypatch):
    location = make_location(tmp_path)
    location.artifact_path.write_bytes(b"artifact")

    original_fstat = os.fstat

    def fail_fstat(descriptor):
        raise OSError(5, "injected fstat failure")

    monkeypatch.setattr(os, "fstat", fail_fstat)

    result = read(location)
    assert result.status is Status.IO_FAILURE

    monkeypatch.setattr(os, "fstat", original_fstat)


def test_read_failure_is_io_failure(tmp_path, monkeypatch):
    location = make_location(tmp_path)
    location.artifact_path.write_bytes(b"artifact")

    original_fdopen = os.fdopen

    class FailingStream:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            raise OSError(5, "injected read failure")

    def fail_fdopen(*args, **kwargs):
        return FailingStream()

    monkeypatch.setattr(os, "fdopen", fail_fdopen)

    result = read(location)
    assert result.status is Status.IO_FAILURE

    monkeypatch.setattr(os, "fdopen", original_fdopen)


def test_close_failure_is_not_unhandled(tmp_path, monkeypatch):
    location = make_location(tmp_path)
    location.artifact_path.write_bytes(b"artifact")

    original_close = os.close

    def fail_close(descriptor):
        original_close(descriptor)
        raise OSError(5, "injected close failure")

    monkeypatch.setattr(os, "close", fail_close)

    result = read(location)
    assert result.status is Status.IO_FAILURE

    monkeypatch.setattr(os, "close", original_close)


def test_replaced_root_must_not_supply_present_artifact(
    tmp_path, monkeypatch
):
    root = tmp_path / "storage"
    replacement = tmp_path / "replacement"
    displaced = tmp_path / "displaced"

    root.mkdir()
    replacement.mkdir()

    location = make_location(root, b"document")

    replacement_artifact = replacement / location.artifact_path.name
    replacement_artifact.write_bytes(
        serialize_product001_documentary_commitment(
            key=location.key,
            content=b"document",
        )
    )

    original_open = os.open
    switched = False

    def replace_root_before_open(path, flags, *args, **kwargs):
        nonlocal switched

        if not switched:
            switched = True
            root.rename(displaced)
            replacement.rename(root)

        return original_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(os, "open", replace_root_before_open)

    result = read(location)

    assert result.status is not Status.PRESENT


def test_root_replaced_after_anchor_cannot_report_absent(
    tmp_path, monkeypatch
):
    root = tmp_path / "storage"
    replacement = tmp_path / "replacement"
    displaced = tmp_path / "displaced"

    root.mkdir()
    replacement.mkdir()

    location = make_location(root)

    original_open = os.open
    switched = False

    def replace_after_anchor(path, flags, *args, **kwargs):
        nonlocal switched

        descriptor = original_open(path, flags, *args, **kwargs)

        if not switched and path == root:
            switched = True
            root.rename(displaced)
            replacement.rename(root)

        return descriptor

    monkeypatch.setattr(os, "open", replace_after_anchor)

    result = read(location)

    assert result.status is Status.IO_FAILURE


def test_root_descriptor_close_failure_is_io_failure(
    tmp_path, monkeypatch
):
    root = tmp_path / "storage"
    root.mkdir()
    location = make_location(root)

    original_open = os.open
    original_close = os.close

    root_descriptor = None
    injected = False

    def capture_open(path, flags, *args, **kwargs):
        nonlocal root_descriptor

        descriptor = original_open(path, flags, *args, **kwargs)

        if path == root:
            root_descriptor = descriptor

        return descriptor

    def fail_root_close(descriptor):
        nonlocal injected

        if descriptor == root_descriptor and not injected:
            injected = True
            original_close(descriptor)
            raise OSError(5, "injected root close failure")

        return original_close(descriptor)

    monkeypatch.setattr(os, "open", capture_open)
    monkeypatch.setattr(os, "close", fail_root_close)

    result = read(location)

    assert injected
    assert result.status is Status.IO_FAILURE
