import ast
import hashlib
import inspect
import re
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_digest_manifest import (
    SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_root import (
    SECURITY_ADMISSION_MERKLE_ALGORITHM,
    SECURITY_ADMISSION_MERKLE_LEAF_PREFIX,
    SECURITY_ADMISSION_MERKLE_NODE_PREFIX,
    SECURITY_ADMISSION_MERKLE_TREE_HASH_PROFILE,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
    build_security_admission_evidence_coverage_closure_state_merkle_root,
)
from sp001.services.security_admission_portable_integer_validation import (
    SECURITY_ADMISSION_PORTABLE_UINT64_MAX,
)
from tests.test_security_admission_evidence_coverage_closure_state_digest_manifest import (
    create_entry,
    create_manifest,
)


def manifest_with_size(
    size: int,
) -> SecurityAdmissionEvidenceCoverageClosureStateDigestManifest:
    return SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
        entries=tuple(
            create_entry(f"coverage-merkle-{index}")
            for index in range(size)
        ),
    )


def leaf_hash(value: str) -> bytes:
    return hashlib.sha256(
        b"\x00" + bytes.fromhex(value)
    ).digest()


def node_hash(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(
        b"\x01" + left + right
    ).digest()


def test_merkle_root_fields_are_exact() -> None:
    root_fields = fields(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot
    )

    assert tuple(field.name for field in root_fields) == (
        "algorithm",
        "tree_hash_profile",
        "leaf_count",
        "value",
    )
    assert tuple(field.type for field in root_fields) == (
        str,
        str,
        int,
        str,
    )


def test_merkle_root_is_immutable_and_slotted() -> None:
    root = (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=create_manifest(),
        )
    )

    assert not hasattr(root, "__dict__")

    with pytest.raises(FrozenInstanceError):
        root.value = "0" * 64  # type: ignore[misc]


def test_merkle_profile_constants_are_exact() -> None:
    assert SECURITY_ADMISSION_MERKLE_ALGORITHM == "SHA-256"
    assert (
        SECURITY_ADMISSION_MERKLE_TREE_HASH_PROFILE
        == "RFC6962"
    )
    assert SECURITY_ADMISSION_MERKLE_LEAF_PREFIX == b"\x00"
    assert SECURITY_ADMISSION_MERKLE_NODE_PREFIX == b"\x01"


def test_single_leaf_matches_independent_vector() -> None:
    manifest = manifest_with_size(1)
    expected = leaf_hash(
        manifest.entries[0].digest.value
    ).hex()

    root = (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=manifest,
        )
    )

    assert root.algorithm == "SHA-256"
    assert root.tree_hash_profile == "RFC6962"
    assert root.leaf_count == 1
    assert root.value == expected


def test_two_leaves_match_independent_vector() -> None:
    manifest = manifest_with_size(2)
    first = leaf_hash(manifest.entries[0].digest.value)
    second = leaf_hash(manifest.entries[1].digest.value)
    expected = node_hash(first, second).hex()

    root = (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=manifest,
        )
    )

    assert root.leaf_count == 2
    assert root.value == expected


def test_three_leaves_use_largest_power_of_two_split() -> None:
    manifest = manifest_with_size(3)
    leaves = tuple(
        leaf_hash(entry.digest.value)
        for entry in manifest.entries
    )
    expected = node_hash(
        node_hash(leaves[0], leaves[1]),
        leaves[2],
    ).hex()

    root = (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=manifest,
        )
    )

    assert root.leaf_count == 3
    assert root.value == expected


def test_five_leaves_use_rfc6962_recursive_split() -> None:
    manifest = manifest_with_size(5)
    leaves = tuple(
        leaf_hash(entry.digest.value)
        for entry in manifest.entries
    )
    left = node_hash(
        node_hash(leaves[0], leaves[1]),
        node_hash(leaves[2], leaves[3]),
    )
    expected = node_hash(left, leaves[4]).hex()

    root = (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=manifest,
        )
    )

    assert root.leaf_count == 5
    assert root.value == expected


@pytest.mark.parametrize("size", (1, 2, 3, 4, 5, 7, 8, 9))
def test_merkle_root_is_deterministic(size: int) -> None:
    manifest = manifest_with_size(size)

    first = (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=manifest,
        )
    )
    second = (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=manifest,
        )
    )

    assert first == second
    assert re.fullmatch(r"[0-9a-f]{64}", first.value)


def test_declared_order_changes_root() -> None:
    manifest = manifest_with_size(3)
    reversed_manifest = (
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
            entries=tuple(reversed(manifest.entries)),
        )
    )

    original = (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=manifest,
        )
    )
    reversed_root = (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=reversed_manifest,
        )
    )

    assert reversed_root.value != original.value


def test_appending_one_leaf_changes_root_and_count() -> None:
    first_manifest = manifest_with_size(2)
    extended_manifest = (
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest(
            entries=(
                *first_manifest.entries,
                create_entry("coverage-merkle-appended"),
            ),
        )
    )

    first = (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=first_manifest,
        )
    )
    extended = (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=extended_manifest,
        )
    )

    assert first.leaf_count == 2
    assert extended.leaf_count == 3
    assert first.value != extended.value


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
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "algorithm",
    (
        "",
        "sha256",
        "SHA-512",
        None,
    ),
)
def test_root_requires_exact_algorithm(
    algorithm: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="algorithm must be SHA-256",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot(
            algorithm=algorithm,  # type: ignore[arg-type]
            tree_hash_profile="RFC6962",
            leaf_count=1,
            value="0" * 64,
        )


@pytest.mark.parametrize(
    "profile",
    (
        "",
        "rfc6962",
        "RFC6962-COMPATIBLE",
        None,
    ),
)
def test_root_requires_exact_tree_hash_profile(
    profile: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="tree_hash_profile must be RFC6962",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot(
            algorithm="SHA-256",
            tree_hash_profile=profile,  # type: ignore[arg-type]
            leaf_count=1,
            value="0" * 64,
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
def test_leaf_count_requires_exact_integer(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="leaf_count must be an integer",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot(
            algorithm="SHA-256",
            tree_hash_profile="RFC6962",
            leaf_count=invalid_value,  # type: ignore[arg-type]
            value="0" * 64,
        )


@pytest.mark.parametrize("invalid_value", (0, -1))
def test_leaf_count_must_be_positive(
    invalid_value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="leaf_count must be positive",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot(
            algorithm="SHA-256",
            tree_hash_profile="RFC6962",
            leaf_count=invalid_value,
            value="0" * 64,
        )


def test_leaf_count_rejects_uint64_overflow() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "leaf_count must not exceed "
            "portable uint64 maximum"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot(
            algorithm="SHA-256",
            tree_hash_profile="RFC6962",
            leaf_count=(
                SECURITY_ADMISSION_PORTABLE_UINT64_MAX + 1
            ),
            value="0" * 64,
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
def test_root_value_requires_lowercase_sha256_hex(
    invalid_value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "value must contain 64 lowercase "
            "hexadecimal characters"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot(
            algorithm="SHA-256",
            tree_hash_profile="RFC6962",
            leaf_count=1,
            value=invalid_value,  # type: ignore[arg-type]
        )


def test_equal_reconstruction_has_value_equality() -> None:
    root = (
        build_security_admission_evidence_coverage_closure_state_merkle_root(
            manifest=create_manifest(),
        )
    )
    reconstructed = replace(root)

    assert reconstructed == root
    assert reconstructed is not root


def test_module_defines_only_root_validation_and_tree_hashing() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot
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
        "build_security_admission_evidence_coverage_closure_state_merkle_root",
        "_merkle_tree_hash",
    }


def test_module_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot
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
        "re",
        "sp001",
    }


def test_root_claims_no_inclusion_consistency_or_consensus() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot
    )
    assert module is not None

    source = inspect.getsource(module).lower()

    for forbidden in (
        "inclusion proof",
        "consistency proof",
        "append-only",
        "consensus",
        "signature",
        "authenticity",
    ):
        assert forbidden not in source
