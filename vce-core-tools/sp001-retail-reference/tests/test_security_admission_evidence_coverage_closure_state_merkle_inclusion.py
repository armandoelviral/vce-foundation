import ast
import hashlib
import inspect
import re
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_digest_manifest import (
    SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
    SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_inclusion import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof,
    build_security_admission_evidence_coverage_closure_state_merkle_inclusion_proof,
    verify_security_admission_evidence_coverage_closure_state_merkle_inclusion,
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


def build_root(
    manifest: SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot:
    return (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=manifest,
        )
    )


def build_proof(
    manifest: SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
    leaf_index: int,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof:
    return (
        build_security_admission_evidence_coverage_closure_state_merkle_inclusion_proof(
            manifest=manifest,
            leaf_index=leaf_index,
        )
    )


def verify(
    entry: SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry,
    proof: SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof,
    root: SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
) -> bool:
    return verify_security_admission_evidence_coverage_closure_state_merkle_inclusion(
        entry=entry,
        proof=proof,
        root=root,
    )


def test_proof_fields_are_exact() -> None:
    proof_fields = fields(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof
    )

    assert tuple(field.name for field in proof_fields) == (
        "leaf_index",
        "leaf_count",
        "audit_path",
    )
    assert tuple(field.type for field in proof_fields) == (
        int,
        int,
        tuple[str, ...],
    )


def test_proof_is_immutable_and_slotted() -> None:
    manifest = manifest_with_size(2)
    proof = build_proof(manifest, 0)

    assert not hasattr(proof, "__dict__")

    with pytest.raises(FrozenInstanceError):
        proof.leaf_index = 1  # type: ignore[misc]


def test_single_leaf_proof_is_empty_and_valid() -> None:
    manifest = manifest_with_size(1)
    proof = build_proof(manifest, 0)
    root = build_root(manifest)

    assert proof.leaf_index == 0
    assert proof.leaf_count == 1
    assert proof.audit_path == ()
    assert verify(manifest.entries[0], proof, root)


@pytest.mark.parametrize("size", (2, 3, 4, 5, 7, 8, 9))
def test_every_manifest_position_has_valid_proof(
    size: int,
) -> None:
    manifest = manifest_with_size(size)
    root = build_root(manifest)

    for index, entry in enumerate(manifest.entries):
        proof = build_proof(manifest, index)

        assert proof.leaf_index == index
        assert proof.leaf_count == size
        assert all(
            re.fullmatch(r"[0-9a-f]{64}", value)
            for value in proof.audit_path
        )
        assert verify(entry, proof, root)


def test_three_leaf_paths_match_independent_vectors() -> None:
    manifest = manifest_with_size(3)
    leaves = tuple(
        leaf_hash(entry.digest.value)
        for entry in manifest.entries
    )
    left_subtree = node_hash(leaves[0], leaves[1])

    assert build_proof(manifest, 0).audit_path == (
        leaves[1].hex(),
        leaves[2].hex(),
    )
    assert build_proof(manifest, 1).audit_path == (
        leaves[0].hex(),
        leaves[2].hex(),
    )
    assert build_proof(manifest, 2).audit_path == (
        left_subtree.hex(),
    )


def test_wrong_entry_fails_verification() -> None:
    manifest = manifest_with_size(3)
    proof = build_proof(manifest, 0)
    root = build_root(manifest)

    assert not verify(
        manifest.entries[1],
        proof,
        root,
    )


def test_wrong_leaf_index_fails_verification() -> None:
    manifest = manifest_with_size(3)
    proof = replace(
        build_proof(manifest, 0),
        leaf_index=1,
    )

    assert not verify(
        manifest.entries[0],
        proof,
        build_root(manifest),
    )


def test_wrong_root_fails_verification() -> None:
    manifest = manifest_with_size(3)
    proof = build_proof(manifest, 0)
    root = build_root(manifest)
    replacement = (
        "0" * 64
        if root.value != "0" * 64
        else "1" * 64
    )
    wrong_root = replace(root, value=replacement)

    assert not verify(
        manifest.entries[0],
        proof,
        wrong_root,
    )


def test_root_leaf_count_mismatch_fails_verification() -> None:
    manifest = manifest_with_size(3)
    proof = build_proof(manifest, 0)
    root = replace(
        build_root(manifest),
        leaf_count=4,
    )

    assert not verify(
        manifest.entries[0],
        proof,
        root,
    )


def test_incomplete_audit_path_fails_closed() -> None:
    manifest = manifest_with_size(5)
    proof = build_proof(manifest, 0)
    incomplete = replace(
        proof,
        audit_path=proof.audit_path[:-1],
    )

    assert not verify(
        manifest.entries[0],
        incomplete,
        build_root(manifest),
    )


def test_surplus_audit_path_fails_closed() -> None:
    manifest = manifest_with_size(5)
    proof = build_proof(manifest, 0)
    surplus = replace(
        proof,
        audit_path=(
            *proof.audit_path,
            "0" * 64,
        ),
    )

    assert not verify(
        manifest.entries[0],
        surplus,
        build_root(manifest),
    )


def test_tampered_audit_hash_fails_closed() -> None:
    manifest = manifest_with_size(5)
    proof = build_proof(manifest, 0)
    replacement = (
        "0" * 64
        if proof.audit_path[0] != "0" * 64
        else "1" * 64
    )
    tampered = replace(
        proof,
        audit_path=(
            replacement,
            *proof.audit_path[1:],
        ),
    )

    assert not verify(
        manifest.entries[0],
        tampered,
        build_root(manifest),
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
def test_builder_requires_nominal_manifest(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "manifest must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateDigestManifest"
        ),
    ):
        build_security_admission_evidence_coverage_closure_state_merkle_inclusion_proof(
            manifest=invalid_value,  # type: ignore[arg-type]
            leaf_index=0,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        True,
        False,
        0.0,
        "0",
        object(),
    ),
)
def test_builder_leaf_index_requires_exact_integer(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="leaf_index must be an integer",
    ):
        build_security_admission_evidence_coverage_closure_state_merkle_inclusion_proof(
            manifest=manifest_with_size(1),
            leaf_index=invalid_value,  # type: ignore[arg-type]
        )


def test_builder_rejects_negative_leaf_index() -> None:
    with pytest.raises(
        ValueError,
        match="leaf_index must be non-negative",
    ):
        build_proof(manifest_with_size(1), -1)


def test_builder_rejects_index_outside_manifest() -> None:
    with pytest.raises(
        ValueError,
        match="leaf_index must identify one manifest entry",
    ):
        build_proof(manifest_with_size(2), 2)


def test_builder_rejects_uint64_index_overflow() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "leaf_index must not exceed "
            "portable uint64 maximum"
        ),
    ):
        build_proof(
            manifest_with_size(1),
            SECURITY_ADMISSION_PORTABLE_UINT64_MAX + 1,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        True,
        False,
        0.0,
        "0",
        object(),
    ),
)
def test_proof_leaf_index_requires_exact_integer(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="leaf_index must be an integer",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof(
            leaf_index=invalid_value,  # type: ignore[arg-type]
            leaf_count=1,
            audit_path=(),
        )


def test_proof_leaf_index_must_be_non_negative() -> None:
    with pytest.raises(
        ValueError,
        match="leaf_index must be non-negative",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof(
            leaf_index=-1,
            leaf_count=1,
            audit_path=(),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        True,
        False,
        1.0,
        "1",
        object(),
    ),
)
def test_proof_leaf_count_requires_exact_integer(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="leaf_count must be an integer",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof(
            leaf_index=0,
            leaf_count=invalid_value,  # type: ignore[arg-type]
            audit_path=(),
        )


@pytest.mark.parametrize("invalid_value", (0, -1))
def test_proof_leaf_count_must_be_positive(
    invalid_value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="leaf_count must be positive",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof(
            leaf_index=0,
            leaf_count=invalid_value,
            audit_path=(),
        )


def test_proof_rejects_index_not_below_count() -> None:
    with pytest.raises(
        ValueError,
        match="leaf_index must be less than leaf_count",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof(
            leaf_index=1,
            leaf_count=1,
            audit_path=(),
        )


def test_proof_rejects_uint64_count_overflow() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "leaf_count must not exceed "
            "portable uint64 maximum"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof(
            leaf_index=0,
            leaf_count=(
                SECURITY_ADMISSION_PORTABLE_UINT64_MAX + 1
            ),
            audit_path=(),
        )


def test_audit_path_requires_immutable_tuple() -> None:
    with pytest.raises(
        TypeError,
        match="audit_path must be an immutable tuple",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof(
            leaf_index=0,
            leaf_count=1,
            audit_path=[],  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        "",
        "0" * 63,
        "0" * 65,
        "A" * 64,
        "g" * 64,
        1,
        True,
        object(),
    ),
)
def test_audit_path_requires_lowercase_sha256_hashes(
    invalid_value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "audit_path must contain 64-character "
            "lowercase hexadecimal hashes"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof(
            leaf_index=0,
            leaf_count=1,
            audit_path=(invalid_value,),  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "argument",
    (
        "entry",
        "proof",
        "root",
    ),
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
def test_verifier_requires_nominal_inputs(
    argument: str,
    invalid_value: object,
) -> None:
    manifest = manifest_with_size(2)
    values = {
        "entry": manifest.entries[0],
        "proof": build_proof(manifest, 0),
        "root": build_root(manifest),
    }
    values[argument] = invalid_value

    expected = {
        "entry": (
            "entry must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry"
        ),
        "proof": (
            "proof must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof"
        ),
        "root": (
            "root must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot"
        ),
    }

    with pytest.raises(TypeError, match=expected[argument]):
        verify_security_admission_evidence_coverage_closure_state_merkle_inclusion(
            entry=values["entry"],  # type: ignore[arg-type]
            proof=values["proof"],  # type: ignore[arg-type]
            root=values["root"],  # type: ignore[arg-type]
        )


def test_verification_is_deterministic() -> None:
    manifest = manifest_with_size(7)
    proof = build_proof(manifest, 4)
    root = build_root(manifest)

    assert verify(manifest.entries[4], proof, root)
    assert verify(manifest.entries[4], proof, root)


def test_module_defines_only_proof_validation_and_verification() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof
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

    assert functions == {
        "__post_init__",
        "build_security_admission_evidence_coverage_closure_state_merkle_inclusion_proof",
        "verify_security_admission_evidence_coverage_closure_state_merkle_inclusion",
        "_inclusion_path",
        "_rebuild_root",
    }


def test_module_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof
    )
    assert module is not None

    tree = ast.parse(inspect.getsource(module))
    roots = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif (
            isinstance(node, ast.ImportFrom)
            and node.module is not None
        ):
            roots.add(node.module.split(".")[0])

    assert roots == {
        "dataclasses",
        "hashlib",
        "hmac",
        "re",
        "sp001",
    }


def test_inclusion_proof_claims_no_consistency_or_consensus() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof
    )
    assert module is not None

    source = inspect.getsource(module).lower()

    for forbidden in (
        "consistency proof",
        "append-only",
        "consensus",
        "signature",
        "authenticity",
    ):
        assert forbidden not in source
