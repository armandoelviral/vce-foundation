import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.services import (
    security_admission_evidence_coverage_closure_state_digest_manifest
    as manifest_module,
)
from sp001.services.security_admission_evidence_coverage_closure_state_digest import (
    SecurityAdmissionEvidenceCoverageClosureStateDigest,
)
from sp001.services.security_admission_evidence_coverage_closure_state_digest_manifest import (
    SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
    SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry,
)
from tests.test_security_admission_evidence_coverage_closure_state_digest import (
    create_record,
    digest_record,
)


def create_entry(
    coverage_id: str = "coverage-manifest-1",
) -> SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry:
    record = create_record()
    coverage_identity = record.closure_resolution.coverage_identity
    object.__setattr__(
        coverage_identity,
        "coverage_id",
        coverage_id,
    )
    digest = digest_record(record)

    return (
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry(
            record=record,
            digest=digest,
        )
    )


def create_manifest(
) -> SecurityAdmissionEvidenceCoverageClosureStateDigestManifest:
    return SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
        entries=(
            create_entry("coverage-manifest-1"),
            create_entry("coverage-manifest-2"),
        ),
    )


def test_entry_fields_are_exact() -> None:
    entry_fields = fields(
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry
    )

    assert tuple(field.name for field in entry_fields) == (
        "record",
        "digest",
    )


def test_manifest_fields_are_exact() -> None:
    manifest_fields = fields(
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest
    )

    assert tuple(field.name for field in manifest_fields) == (
        "entries",
    )
    assert (
        manifest_fields[0].type
        == tuple[
            SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry,
            ...,
        ]
    )


def test_entry_and_manifest_are_immutable_and_slotted() -> None:
    entry = create_entry()
    manifest = SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
        entries=(entry,),
    )

    assert not hasattr(entry, "__dict__")
    assert not hasattr(manifest, "__dict__")

    with pytest.raises(FrozenInstanceError):
        entry.digest = entry.digest  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        manifest.entries = ()  # type: ignore[misc]


def test_exact_references_are_preserved() -> None:
    entry = create_entry()
    manifest = SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
        entries=(entry,),
    )

    assert manifest.entries[0] is entry
    assert entry.record is entry.record
    assert entry.digest is entry.digest


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        object(),
    ),
)
def test_entry_record_requires_nominal_type(
    invalid_value: object,
) -> None:
    entry = create_entry()

    with pytest.raises(
        TypeError,
        match=(
            "record must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateRecord"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry(
            record=invalid_value,  # type: ignore[arg-type]
            digest=entry.digest,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        object(),
    ),
)
def test_entry_digest_requires_nominal_type(
    invalid_value: object,
) -> None:
    entry = create_entry()

    with pytest.raises(
        TypeError,
        match=(
            "digest must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateDigest"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry(
            record=entry.record,
            digest=invalid_value,  # type: ignore[arg-type]
        )


def test_entry_rejects_digest_from_different_record() -> None:
    first = create_entry("coverage-manifest-1")
    second = create_entry("coverage-manifest-2")

    with pytest.raises(
        ValueError,
        match=(
            "digest must correspond to the exact "
            "closure-state record"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry(
            record=first.record,
            digest=second.digest,
        )


@pytest.mark.parametrize(
    "digest",
    (
        SecurityAdmissionEvidenceCoverageClosureStateDigest(
            algorithm="SHA-512",
            encoding="UTF-8",
            value="0" * 64,
        ),
        SecurityAdmissionEvidenceCoverageClosureStateDigest(
            algorithm="SHA-256",
            encoding="UTF-16",
            value="0" * 64,
        ),
        SecurityAdmissionEvidenceCoverageClosureStateDigest(
            algorithm="SHA-256",
            encoding="UTF-8",
            value="invalid",
        ),
    ),
)
def test_entry_fails_closed_on_invalid_digest_metadata(
    digest: SecurityAdmissionEvidenceCoverageClosureStateDigest,
) -> None:
    entry = create_entry()

    with pytest.raises(ValueError):
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry(
            record=entry.record,
            digest=digest,
        )


def test_manifest_requires_immutable_tuple() -> None:
    entry = create_entry()

    with pytest.raises(
        TypeError,
        match="entries must be an immutable tuple",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
            entries=[entry],  # type: ignore[arg-type]
        )


def test_manifest_rejects_empty_universe() -> None:
    with pytest.raises(
        ValueError,
        match="entries must not be empty",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
            entries=(),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        object(),
    ),
)
def test_manifest_requires_nominal_entries(
    invalid_value: object,
) -> None:
    valid = create_entry()

    with pytest.raises(
        TypeError,
        match=(
            "entries must contain "
            "SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry "
            "values"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
            entries=(
                valid,
                invalid_value,  # type: ignore[arg-type]
            ),
        )


def test_manifest_preserves_declared_order() -> None:
    first = create_entry("coverage-manifest-1")
    second = create_entry("coverage-manifest-2")
    third = create_entry("coverage-manifest-3")

    manifest = (
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
            entries=(second, first, third),
        )
    )

    assert manifest.entries == (
        second,
        first,
        third,
    )
    assert tuple(
        entry.record.closure_resolution.coverage_identity.coverage_id
        for entry in manifest.entries
    ) == (
        "coverage-manifest-2",
        "coverage-manifest-1",
        "coverage-manifest-3",
    )


def test_manifest_rejects_duplicate_coverage_occurrence() -> None:
    entry = create_entry("coverage-manifest-1")

    with pytest.raises(
        ValueError,
        match=r"duplicate coverage occurrence: coverage-manifest-1 1",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
            entries=(entry, entry),
        )


def test_same_coverage_id_with_different_version_is_distinct() -> None:
    first = create_entry("coverage-manifest")
    second = create_entry("coverage-manifest")
    second_identity = (
        second.record.closure_resolution.coverage_identity
    )
    object.__setattr__(
        second_identity,
        "coverage_version",
        2,
    )
    second_digest = digest_record(second.record)
    second = (
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry(
            record=second.record,
            digest=second_digest,
        )
    )

    manifest = (
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
            entries=(first, second),
        )
    )

    assert manifest.entries == (first, second)


def test_one_failed_verification_prevents_entry_construction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    valid = create_entry()

    monkeypatch.setattr(
        manifest_module,
        "verify_security_admission_evidence_coverage_closure_state_digest",
        lambda **kwargs: False,
    )

    with pytest.raises(
        ValueError,
        match=(
            "digest must correspond to the exact "
            "closure-state record"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry(
            record=valid.record,
            digest=valid.digest,
        )


def test_equal_reconstruction_has_value_equality() -> None:
    manifest = create_manifest()
    reconstructed = replace(
        manifest,
        entries=tuple(
            replace(entry)
            for entry in manifest.entries
        ),
    )

    assert reconstructed == manifest
    assert reconstructed is not manifest


def test_module_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest
    )
    assert module is not None

    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        )
    }

    assert functions == {"__post_init__"}


def test_module_imports_only_internal_capabilities() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest
    )
    assert module is not None

    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if (
            isinstance(node, ast.ImportFrom)
            and node.module is not None
        )
    }

    assert roots == {"dataclasses", "sp001"}


def test_manifest_claims_no_merkle_ledger_or_authenticity() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest
    )
    assert module is not None

    source = inspect.getsource(module).lower()

    for forbidden in (
        "merkle",
        "ledger",
        "signature",
        "authenticity",
        "consensus",
    ):
        assert forbidden not in source
