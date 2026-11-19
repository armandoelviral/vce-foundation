"""Functional tests for exclusive documentary publication."""

import hashlib

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
    Product001DocumentaryCommitmentStatus,
)
from sp001.contracts.product001_documentary_commitment_storage_errors import (
    DocumentaryCommitmentConflictError,
    DocumentaryCommitmentStoredArtifactError,
)
from sp001.contracts.product001_documentary_commitment_storage_location import (
    Product001DocumentaryCommitmentStorageLocation,
)
from sp001.services.product001_documentary_commitment_storage import (
    write_product001_documentary_commitment,
)
from sp001.services.product001_documentary_commitment_serialization import (
    deserialize_product001_documentary_commitment,
)


def make_location(root, content=b"original"):
    key = Product001DocumentaryCommitmentKey(
        organization_id="ORG",
        source_identity=KnowledgeSourceIdentity(
            source_id="SOURCE",
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


def test_first_publication_creates_artifact(tmp_path):
    content = b"\x00original\xff"
    location = make_location(tmp_path, content)

    result = write_product001_documentary_commitment(
        location=location,
        content=content,
    )

    assert result.status is Product001DocumentaryCommitmentStatus.CREATED
    assert result.bytes_committed == len(content)

    stored_key, stored_content = (
        deserialize_product001_documentary_commitment(
            location.artifact_path.read_bytes()
        )
    )

    assert stored_key == location.key
    assert stored_content == content


def test_identical_repetition_is_idempotent(tmp_path):
    content = b"original"
    location = make_location(tmp_path, content)

    write_product001_documentary_commitment(
        location=location,
        content=content,
    )
    original_artifact = location.artifact_path.read_bytes()

    result = write_product001_documentary_commitment(
        location=location,
        content=content,
    )

    assert (
        result.status
        is Product001DocumentaryCommitmentStatus.ALREADY_PRESENT
    )
    assert location.artifact_path.read_bytes() == original_artifact


def test_same_identity_different_content_is_conflict(tmp_path):
    first = make_location(tmp_path, b"original")
    second = make_location(tmp_path, b"modified")

    assert first.artifact_path == second.artifact_path

    write_product001_documentary_commitment(
        location=first,
        content=b"original",
    )

    with pytest.raises(DocumentaryCommitmentConflictError):
        write_product001_documentary_commitment(
            location=second,
            content=b"modified",
        )

    _, stored_content = deserialize_product001_documentary_commitment(
        first.artifact_path.read_bytes()
    )
    assert stored_content == b"original"


def test_corrupt_existing_artifact_is_rejected(tmp_path):
    location = make_location(tmp_path)
    location.artifact_path.write_bytes(b"corrupt")

    with pytest.raises(DocumentaryCommitmentStoredArtifactError):
        write_product001_documentary_commitment(
            location=location,
            content=b"original",
        )

    assert location.artifact_path.read_bytes() == b"corrupt"


def test_wrong_input_digest_is_rejected_before_publication(tmp_path):
    location = make_location(tmp_path, b"original")

    with pytest.raises(ValueError):
        write_product001_documentary_commitment(
            location=location,
            content=b"modified",
        )

    assert not location.artifact_path.exists()


def test_missing_storage_directory_is_rejected(tmp_path):
    root = tmp_path / "missing"
    location = make_location(root)

    with pytest.raises(ValueError):
        write_product001_documentary_commitment(
            location=location,
            content=b"original",
        )

    assert not root.exists()


def _concurrent_publish(root, content, start, results):
    """Worker for real multiprocess publication."""
    start.wait()

    try:
        location = make_location(root, content)
        result = write_product001_documentary_commitment(
            location=location,
            content=content,
        )
        results.put(result.status.value)
    except Exception as error:
        results.put(type(error).__name__)


def _run_concurrent_publications(tmp_path, first, second):
    import multiprocessing

    context = multiprocessing.get_context("spawn")
    start = context.Event()
    results = context.Queue()

    processes = [
        context.Process(
            target=_concurrent_publish,
            args=(tmp_path, content, start, results),
        )
        for content in (first, second)
    ]

    for process in processes:
        process.start()

    start.set()

    outcomes = [results.get(timeout=15) for _ in processes]

    for process in processes:
        process.join(timeout=15)
        assert process.exitcode == 0

    return outcomes


def test_concurrent_identical_publications(tmp_path):
    outcomes = _run_concurrent_publications(
        tmp_path,
        b"same",
        b"same",
    )

    assert sorted(outcomes) == [
        "ALREADY_PRESENT",
        "CREATED",
    ]


def test_concurrent_conflicting_publications(tmp_path):
    outcomes = _run_concurrent_publications(
        tmp_path,
        b"first",
        b"second",
    )

    assert sorted(outcomes) == [
        "CREATED",
        "DocumentaryCommitmentConflictError",
    ]

    location = make_location(tmp_path, b"first")
    _, stored = deserialize_product001_documentary_commitment(
        location.artifact_path.read_bytes()
    )
    assert stored in (b"first", b"second")


def test_directory_fsync_failure_is_indeterminate(
    tmp_path, monkeypatch
):
    import os

    import sp001.services.product001_documentary_commitment_storage as storage

    location = make_location(tmp_path)

    def fail_fsync(directory):
        raise OSError("injected directory sync failure")

    monkeypatch.setattr(
        storage,
        "_fsync_directory",
        fail_fsync,
    )

    from sp001.contracts.product001_documentary_commitment_storage_errors import (
        DocumentaryCommitmentPublicationIndeterminateError,
    )

    with pytest.raises(
        DocumentaryCommitmentPublicationIndeterminateError
    ):
        write_product001_documentary_commitment(
            location=location,
            content=b"original",
        )

    assert location.artifact_path.exists()


def test_symbolic_link_destination_is_rejected(tmp_path):
    target = tmp_path / "external.bin"
    target.write_bytes(b"external")

    location = make_location(tmp_path)
    location.artifact_path.symlink_to(target)

    with pytest.raises(DocumentaryCommitmentStoredArtifactError):
        write_product001_documentary_commitment(
            location=location,
            content=b"original",
        )

    assert target.read_bytes() == b"external"


def test_temporary_write_failure_is_storage_io(
    tmp_path, monkeypatch
):
    import tempfile

    import sp001.services.product001_documentary_commitment_storage as storage

    from sp001.contracts.product001_documentary_commitment_storage_errors import (
        DocumentaryCommitmentStorageIOError,
    )

    def fail_temporary(*args, **kwargs):
        raise OSError("injected temporary creation failure")

    monkeypatch.setattr(
        storage.tempfile,
        "NamedTemporaryFile",
        fail_temporary,
    )

    location = make_location(tmp_path)

    with pytest.raises(DocumentaryCommitmentStorageIOError):
        write_product001_documentary_commitment(
            location=location,
            content=b"original",
        )

    assert not location.artifact_path.exists()


def test_link_failure_is_not_reported_as_success(
    tmp_path, monkeypatch
):
    import sp001.services.product001_documentary_commitment_storage as storage

    from sp001.contracts.product001_documentary_commitment_storage_errors import (
        Product001DocumentaryCommitmentStorageError,
    )

    def fail_link(*args, **kwargs):
        raise PermissionError("injected link failure")

    monkeypatch.setattr(storage.os, "link", fail_link)

    location = make_location(tmp_path)

    with pytest.raises(Product001DocumentaryCommitmentStorageError):
        write_product001_documentary_commitment(
            location=location,
            content=b"original",
        )

    assert not location.artifact_path.exists()


def test_existing_artifact_read_io_is_not_corruption(
    tmp_path, monkeypatch
):
    import sp001.services.product001_documentary_commitment_storage as storage

    from sp001.contracts.product001_documentary_commitment_storage_errors import (
        DocumentaryCommitmentStorageIOError,
    )

    location = make_location(tmp_path)

    write_product001_documentary_commitment(
        location=location,
        content=b"original",
    )

    original_open = storage.os.open

    def fail_existing_open(path, flags, *args, **kwargs):
        if str(path) == str(location.artifact_path):
            raise PermissionError("injected existing read failure")
        return original_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(storage.os, "open", fail_existing_open)

    with pytest.raises(DocumentaryCommitmentStorageIOError):
        write_product001_documentary_commitment(
            location=location,
            content=b"original",
        )


def test_cleanup_failure_preserves_primary_exception(
    tmp_path, monkeypatch
):
    import pathlib

    import sp001.services.product001_documentary_commitment_storage as storage

    from sp001.contracts.product001_documentary_commitment_storage_errors import (
        DocumentaryCommitmentPublicationIndeterminateError,
    )

    original_unlink = pathlib.Path.unlink

    def fail_cleanup(self, *args, **kwargs):
        if self.name.startswith(".product001-"):
            raise PermissionError("injected cleanup failure")
        return original_unlink(self, *args, **kwargs)

    def fail_link(*args, **kwargs):
        raise PermissionError("injected publication failure")

    monkeypatch.setattr(pathlib.Path, "unlink", fail_cleanup)
    monkeypatch.setattr(storage.os, "link", fail_link)

    location = make_location(tmp_path)

    with pytest.raises(
        DocumentaryCommitmentPublicationIndeterminateError
    ) as captured:
        write_product001_documentary_commitment(
            location=location,
            content=b"original",
        )

    assert (
        "exclusive documentary publication outcome is unconfirmed"
        in str(captured.value)
    )


def test_link_error_after_destination_creation_is_indeterminate(
    tmp_path, monkeypatch
):
    import os

    import sp001.services.product001_documentary_commitment_storage as storage

    from sp001.contracts.product001_documentary_commitment_storage_errors import (
        DocumentaryCommitmentPublicationIndeterminateError,
    )

    location = make_location(tmp_path)
    original_link = os.link

    def publish_then_fail(source, destination):
        original_link(source, destination)
        raise OSError("injected ambiguous publication result")

    monkeypatch.setattr(storage.os, "link", publish_then_fail)

    with pytest.raises(
        DocumentaryCommitmentPublicationIndeterminateError
    ):
        write_product001_documentary_commitment(
            location=location,
            content=b"original",
        )

    assert location.artifact_path.exists()

    stored_key, stored_content = (
        deserialize_product001_documentary_commitment(
            location.artifact_path.read_bytes()
        )
    )

    assert stored_key.exclusive_identity == (
        location.key.exclusive_identity
    )
    assert stored_content == b"original"


def test_cleanup_failure_after_publication_is_indeterminate(
    tmp_path, monkeypatch
):
    import pathlib

    from sp001.contracts.product001_documentary_commitment_storage_errors import (
        DocumentaryCommitmentPublicationIndeterminateError,
    )

    original_unlink = pathlib.Path.unlink

    def fail_cleanup(self, *args, **kwargs):
        if self.name.startswith(".product001-"):
            raise PermissionError(
                "injected post-publication cleanup failure"
            )
        return original_unlink(self, *args, **kwargs)

    monkeypatch.setattr(
        pathlib.Path,
        "unlink",
        fail_cleanup,
    )

    location = make_location(tmp_path)

    with pytest.raises(
        DocumentaryCommitmentPublicationIndeterminateError
    ) as captured:
        write_product001_documentary_commitment(
            location=location,
            content=b"original",
        )

    assert "temporary cleanup failed" in str(captured.value)

    assert location.artifact_path.exists()

    stored_key, stored_content = (
        deserialize_product001_documentary_commitment(
            location.artifact_path.read_bytes()
        )
    )

    assert (
        stored_key.exclusive_identity
        == location.key.exclusive_identity
    )
    assert stored_content == b"original"


def test_normal_publication_leaves_no_temporary_files(tmp_path):
    location = make_location(tmp_path)

    first = write_product001_documentary_commitment(
        location=location,
        content=b"original",
    )

    assert first.status.value == "CREATED"
    assert not list(tmp_path.glob(".product001-*.tmp"))

    repeated = write_product001_documentary_commitment(
        location=location,
        content=b"original",
    )

    assert repeated.status.value == "ALREADY_PRESENT"
    assert not list(tmp_path.glob(".product001-*.tmp"))
