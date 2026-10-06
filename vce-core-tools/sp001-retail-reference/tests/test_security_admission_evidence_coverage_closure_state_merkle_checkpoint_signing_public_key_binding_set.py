import inspect
from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding import (
    create_binding,
)


def binding(
    index: int,
):
    return create_binding(
        scalar=index,
        key_id=(
            f"kms://security-admission/"
            f"key-{index:03d}"
        ),
    )


def create_binding_set(
    size: int = 3,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet:
    return SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet(
        bindings=tuple(
            binding(index)
            for index in range(1, size + 1)
        ),
    )


def test_binding_set_has_exact_field() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet
        )
    ) == ("bindings",)


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        5,
        8,
    ),
)
def test_canonical_binding_sets_are_accepted(
    size: int,
) -> None:
    binding_set = create_binding_set(
        size=size,
    )

    assert len(binding_set.bindings) == size


def test_binding_set_preserves_exact_tuple() -> None:
    bindings = (
        binding(1),
        binding(2),
        binding(3),
    )

    binding_set = SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet(
        bindings=bindings,
    )

    assert binding_set.bindings is bindings


def test_binding_set_preserves_exact_members() -> None:
    first = binding(1)
    second = binding(2)

    binding_set = SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet(
        bindings=(first, second),
    )

    assert binding_set.bindings[0] is first
    assert binding_set.bindings[1] is second


def test_binding_set_is_frozen() -> None:
    binding_set = create_binding_set()

    with pytest.raises(FrozenInstanceError):
        binding_set.bindings = (binding(4),)


def test_binding_set_uses_slots() -> None:
    binding_set = create_binding_set()

    assert not hasattr(binding_set, "__dict__")


def test_equal_values_are_equal() -> None:
    assert create_binding_set() == create_binding_set()


def test_different_values_are_not_equal() -> None:
    assert create_binding_set(2) != create_binding_set(3)


@pytest.mark.parametrize(
    "value",
    (
        None,
        [],
        {},
        set(),
        "bindings",
        b"bindings",
        1,
        True,
        object(),
    ),
)
def test_bindings_reject_non_tuple(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="bindings must be a tuple",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet(
            bindings=value,
        )


def test_bindings_reject_empty_tuple() -> None:
    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet(
            bindings=(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "binding",
        b"binding",
        1,
        True,
        (),
    ),
)
def test_bindings_reject_invalid_member(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="bindings must contain only",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet(
            bindings=(
                binding(1),
                value,
            ),
        )


def test_duplicate_key_identifier_is_rejected() -> None:
    first = create_binding(
        scalar=1,
        key_id="kms://security-admission/key-001",
    )
    second = create_binding(
        scalar=2,
        key_id="kms://security-admission/key-001",
    )

    with pytest.raises(
        ValueError,
        match="unique key identifiers",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet(
            bindings=(first, second),
        )


def test_duplicate_binding_is_rejected_by_key_identifier() -> None:
    repeated = binding(1)

    with pytest.raises(
        ValueError,
        match="unique key identifiers",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet(
            bindings=(repeated, repeated),
        )


def test_noncanonical_key_identifier_order_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="canonical key identifier order",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet(
            bindings=(
                binding(2),
                binding(1),
            ),
        )


def test_reverse_order_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="canonical key identifier order",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet(
            bindings=(
                binding(3),
                binding(2),
                binding(1),
            ),
        )


def test_duplicate_public_key_fingerprint_is_rejected() -> None:
    first = create_binding(
        scalar=7,
        key_id="kms://security-admission/key-001",
    )
    second = create_binding(
        scalar=7,
        key_id="kms://security-admission/key-002",
    )

    with pytest.raises(
        ValueError,
        match="unique public-key fingerprints",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet(
            bindings=(first, second),
        )


def test_distinct_keys_have_distinct_fingerprints() -> None:
    binding_set = create_binding_set(
        size=5,
    )
    fingerprints = tuple(
        item
        .signing_key_identity
        .public_key_fingerprint
        for item in binding_set.bindings
    )

    assert len(fingerprints) == len(
        set(fingerprints)
    )


def test_key_identifiers_are_canonically_ordered() -> None:
    binding_set = create_binding_set(
        size=5,
    )
    key_ids = tuple(
        item.signing_key_identity.key_id
        for item in binding_set.bindings
    )

    assert key_ids == tuple(sorted(key_ids))


def test_binding_set_contains_no_private_key() -> None:
    field_names = tuple(
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet
        )
    )
    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet
    )

    assert "private_key" not in field_names
    assert "private_bytes" not in source


def test_binding_set_does_not_resolve_or_verify() -> None:
    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet
    ).lower()
    forbidden = (
        "resolve",
        "verify",
        "signature",
        "admission_decision",
        "authorization",
        "authority",
        "rejection",
    )

    assert all(
        token not in source
        for token in forbidden
    )
