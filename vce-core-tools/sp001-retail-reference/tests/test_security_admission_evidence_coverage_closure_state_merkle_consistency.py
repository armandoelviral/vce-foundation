import ast
import inspect
import re
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_digest_manifest import (
    SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_consistency import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof,
    build_security_admission_evidence_coverage_closure_state_merkle_consistency_proof,
    verify_security_admission_evidence_coverage_closure_state_merkle_consistency,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_root import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
    build_security_admission_evidence_coverage_closure_state_merkle_root,
)
from sp001.services.security_admission_portable_integer_validation import (
    SECURITY_ADMISSION_PORTABLE_UINT64_MAX,
)
from tests.test_security_admission_evidence_coverage_closure_state_digest_manifest import (
    create_entry,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_root import (
    leaf_hash,
    manifest_with_size,
    node_hash,
)


def prefix_manifest(
    manifest: SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
    size: int,
) -> SecurityAdmissionEvidenceCoverageClosureStateDigestManifest:
    return SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
        entries=manifest.entries[:size],
    )


def build_root(
    manifest: SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot:
    return (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=manifest,
        )
    )


def build_proof(
    old_manifest: SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
    new_manifest: SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof:
    return (
        build_security_admission_evidence_coverage_closure_state_merkle_consistency_proof(
            old_manifest=old_manifest,
            new_manifest=new_manifest,
        )
    )


def verify(
    old_root: SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
    new_root: SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
    proof: SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof,
) -> bool:
    return verify_security_admission_evidence_coverage_closure_state_merkle_consistency(
        old_root=old_root,
        new_root=new_root,
        proof=proof,
    )


def test_proof_fields_are_exact() -> None:
    proof_fields = fields(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof
    )

    assert tuple(field.name for field in proof_fields) == (
        "old_leaf_count",
        "new_leaf_count",
        "audit_path",
    )
    assert tuple(field.type for field in proof_fields) == (
        int,
        int,
        tuple[str, ...],
    )


def test_proof_is_immutable_and_slotted() -> None:
    manifest = manifest_with_size(2)
    proof = build_proof(
        prefix_manifest(manifest, 1),
        manifest,
    )

    assert not hasattr(proof, "__dict__")

    with pytest.raises(FrozenInstanceError):
        proof.old_leaf_count = 2  # type: ignore[misc]


@pytest.mark.parametrize(
    ("old_size", "new_size"),
    (
        (1, 2),
        (1, 3),
        (2, 3),
        (1, 4),
        (2, 4),
        (3, 4),
        (1, 5),
        (2, 5),
        (3, 5),
        (4, 5),
        (1, 7),
        (2, 7),
        (3, 7),
        (4, 7),
        (5, 7),
        (6, 7),
        (1, 8),
        (3, 8),
        (4, 8),
        (7, 8),
        (1, 9),
        (4, 9),
        (8, 9),
    ),
)
def test_every_strict_prefix_has_valid_consistency_proof(
    old_size: int,
    new_size: int,
) -> None:
    new_manifest = manifest_with_size(new_size)
    old_manifest = prefix_manifest(
        new_manifest,
        old_size,
    )

    proof = build_proof(
        old_manifest,
        new_manifest,
    )

    assert proof.old_leaf_count == old_size
    assert proof.new_leaf_count == new_size
    assert proof.audit_path
    assert all(
        re.fullmatch(r"[0-9a-f]{64}", value)
        for value in proof.audit_path
    )
    assert verify(
        build_root(old_manifest),
        build_root(new_manifest),
        proof,
    )


def test_rfc6962_three_of_seven_vector_is_exact() -> None:
    manifest = manifest_with_size(7)
    leaves = tuple(
        leaf_hash(entry.digest.value)
        for entry in manifest.entries
    )

    c = leaves[2]
    d = leaves[3]
    g = node_hash(leaves[0], leaves[1])
    i = node_hash(leaves[4], leaves[5])
    l = node_hash(i, leaves[6])

    proof = build_proof(
        prefix_manifest(manifest, 3),
        manifest,
    )

    assert proof.audit_path == (
        c.hex(),
        d.hex(),
        g.hex(),
        l.hex(),
    )


def test_rfc6962_four_of_seven_vector_is_exact() -> None:
    manifest = manifest_with_size(7)
    leaves = tuple(
        leaf_hash(entry.digest.value)
        for entry in manifest.entries
    )

    i = node_hash(leaves[4], leaves[5])
    l = node_hash(i, leaves[6])

    proof = build_proof(
        prefix_manifest(manifest, 4),
        manifest,
    )

    assert proof.audit_path == (l.hex(),)


def test_rfc6962_six_of_seven_vector_is_exact() -> None:
    manifest = manifest_with_size(7)
    leaves = tuple(
        leaf_hash(entry.digest.value)
        for entry in manifest.entries
    )

    i = node_hash(leaves[4], leaves[5])
    j = leaves[6]
    g = node_hash(leaves[0], leaves[1])
    h = node_hash(leaves[2], leaves[3])
    k = node_hash(g, h)

    proof = build_proof(
        prefix_manifest(manifest, 6),
        manifest,
    )

    assert proof.audit_path == (
        i.hex(),
        j.hex(),
        k.hex(),
    )


def test_builder_preserves_manifest_without_mutation() -> None:
    new_manifest = manifest_with_size(4)
    old_manifest = prefix_manifest(new_manifest, 2)
    old_entries = old_manifest.entries
    new_entries = new_manifest.entries

    build_proof(old_manifest, new_manifest)

    assert old_manifest.entries is old_entries
    assert new_manifest.entries is new_entries


def test_builder_rejects_equal_manifest_sizes() -> None:
    manifest = manifest_with_size(2)

    with pytest.raises(
        ValueError,
        match=(
            "old_manifest must contain fewer entries "
            "than new_manifest"
        ),
    ):
        build_proof(manifest, manifest)


def test_builder_rejects_reversed_manifest_sizes() -> None:
    larger = manifest_with_size(3)
    smaller = prefix_manifest(larger, 2)

    with pytest.raises(
        ValueError,
        match=(
            "old_manifest must contain fewer entries "
            "than new_manifest"
        ),
    ):
        build_proof(larger, smaller)


def test_builder_rejects_divergent_old_manifest() -> None:
    new_manifest = manifest_with_size(3)
    divergent = SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
        entries=(
            create_entry("coverage-divergent"),
            new_manifest.entries[1],
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "old_manifest must be an exact ordered prefix "
            "of new_manifest"
        ),
    ):
        build_proof(divergent, new_manifest)


def test_builder_rejects_reordered_old_manifest() -> None:
    new_manifest = manifest_with_size(3)
    reordered = SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
        entries=(
            new_manifest.entries[1],
            new_manifest.entries[0],
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "old_manifest must be an exact ordered prefix "
            "of new_manifest"
        ),
    ):
        build_proof(reordered, new_manifest)


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        object(),
    ),
)
def test_builder_requires_nominal_old_manifest(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "old_manifest must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateDigestManifest"
        ),
    ):
        build_security_admission_evidence_coverage_closure_state_merkle_consistency_proof(
            old_manifest=invalid_value,  # type: ignore[arg-type]
            new_manifest=manifest_with_size(2),
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
def test_builder_requires_nominal_new_manifest(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "new_manifest must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateDigestManifest"
        ),
    ):
        build_security_admission_evidence_coverage_closure_state_merkle_consistency_proof(
            old_manifest=manifest_with_size(1),
            new_manifest=invalid_value,  # type: ignore[arg-type]
        )


def test_tampered_audit_hash_fails_closed() -> None:
    new_manifest = manifest_with_size(7)
    old_manifest = prefix_manifest(new_manifest, 3)
    proof = build_proof(old_manifest, new_manifest)

    tampered = replace(
        proof,
        audit_path=(
            "0" * 64,
            *proof.audit_path[1:],
        ),
    )

    assert not verify(
        build_root(old_manifest),
        build_root(new_manifest),
        tampered,
    )


def test_truncated_audit_path_fails_closed() -> None:
    new_manifest = manifest_with_size(7)
    old_manifest = prefix_manifest(new_manifest, 3)
    proof = build_proof(old_manifest, new_manifest)

    truncated = replace(
        proof,
        audit_path=proof.audit_path[:-1],
    )

    assert not verify(
        build_root(old_manifest),
        build_root(new_manifest),
        truncated,
    )


def test_surplus_audit_hash_fails_closed() -> None:
    new_manifest = manifest_with_size(7)
    old_manifest = prefix_manifest(new_manifest, 3)
    proof = build_proof(old_manifest, new_manifest)

    surplus = replace(
        proof,
        audit_path=proof.audit_path + ("0" * 64,),
    )

    assert not verify(
        build_root(old_manifest),
        build_root(new_manifest),
        surplus,
    )


def test_wrong_old_root_fails_closed() -> None:
    new_manifest = manifest_with_size(7)
    old_manifest = prefix_manifest(new_manifest, 3)
    proof = build_proof(old_manifest, new_manifest)
    wrong_old_root = replace(
        build_root(old_manifest),
        value="0" * 64,
    )

    assert not verify(
        wrong_old_root,
        build_root(new_manifest),
        proof,
    )


def test_wrong_new_root_fails_closed() -> None:
    new_manifest = manifest_with_size(7)
    old_manifest = prefix_manifest(new_manifest, 3)
    proof = build_proof(old_manifest, new_manifest)
    new_root = build_root(new_manifest)
    wrong_new_root = replace(
        new_root,
        value="0" * 64,
    )

    assert not verify(
        build_root(old_manifest),
        wrong_new_root,
        proof,
    )


def test_root_count_mismatch_fails_closed() -> None:
    new_manifest = manifest_with_size(7)
    old_manifest = prefix_manifest(new_manifest, 3)
    proof = build_proof(old_manifest, new_manifest)

    mismatched = replace(
        proof,
        old_leaf_count=2,
    )

    assert not verify(
        build_root(old_manifest),
        build_root(new_manifest),
        mismatched,
    )


@pytest.mark.parametrize(
    "invalid_count",
    (
        None,
        True,
        1.0,
        "1",
    ),
)
def test_proof_counts_require_exact_integers(
    invalid_count: object,
) -> None:
    with pytest.raises(TypeError):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof(
            old_leaf_count=invalid_count,  # type: ignore[arg-type]
            new_leaf_count=2,
            audit_path=("0" * 64,),
        )


@pytest.mark.parametrize(
    "invalid_count",
    (
        0,
        -1,
        SECURITY_ADMISSION_PORTABLE_UINT64_MAX + 1,
    ),
)
def test_proof_counts_require_positive_uint64(
    invalid_count: int,
) -> None:
    with pytest.raises(ValueError):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof(
            old_leaf_count=invalid_count,
            new_leaf_count=2,
            audit_path=("0" * 64,),
        )


def test_proof_requires_strict_extension() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "old_leaf_count must be less than new_leaf_count"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof(
            old_leaf_count=2,
            new_leaf_count=2,
            audit_path=("0" * 64,),
        )


@pytest.mark.parametrize(
    "invalid_path",
    (
        [],
        "0" * 64,
        None,
    ),
)
def test_audit_path_requires_tuple(
    invalid_path: object,
) -> None:
    with pytest.raises(TypeError):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof(
            old_leaf_count=1,
            new_leaf_count=2,
            audit_path=invalid_path,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "invalid_hash",
    (
        "",
        "0" * 63,
        "0" * 65,
        "A" * 64,
        "g" * 64,
        1,
        None,
    ),
)
def test_audit_path_requires_canonical_hashes(
    invalid_hash: object,
) -> None:
    with pytest.raises(ValueError):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof(
            old_leaf_count=1,
            new_leaf_count=2,
            audit_path=(invalid_hash,),  # type: ignore[arg-type]
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
def test_verifier_requires_nominal_old_root(
    invalid_value: object,
) -> None:
    manifest = manifest_with_size(2)
    proof = build_proof(
        prefix_manifest(manifest, 1),
        manifest,
    )

    with pytest.raises(TypeError):
        verify_security_admission_evidence_coverage_closure_state_merkle_consistency(
            old_root=invalid_value,  # type: ignore[arg-type]
            new_root=build_root(manifest),
            proof=proof,
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
def test_verifier_requires_nominal_proof(
    invalid_value: object,
) -> None:
    manifest = manifest_with_size(2)

    with pytest.raises(TypeError):
        verify_security_admission_evidence_coverage_closure_state_merkle_consistency(
            old_root=build_root(prefix_manifest(manifest, 1)),
            new_root=build_root(manifest),
            proof=invalid_value,  # type: ignore[arg-type]
        )


def test_consistency_service_has_no_signing_or_authority_capability() -> None:
    source = inspect.getsource(
        build_security_admission_evidence_coverage_closure_state_merkle_consistency_proof
    )
    source += inspect.getsource(
        verify_security_admission_evidence_coverage_closure_state_merkle_consistency
    )

    tree = ast.parse(source)
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
        )
    }

    assert "sign" not in called_names
    assert "authorize" not in called_names
    assert "admit" not in called_names
    assert "decide" not in called_names
