import inspect
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding_resolution import (
    resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding import (
    create_binding,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding_set import (
    binding,
    create_binding_set,
)


@pytest.mark.parametrize(
    "index",
    (
        1,
        2,
        3,
        4,
        5,
    ),
)
def test_exact_identity_resolves_exact_binding(
    index: int,
) -> None:
    binding_set = create_binding_set(
        size=5,
    )
    expected = binding_set.bindings[
        index - 1
    ]

    resolved = (
        resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding(
            binding_set=binding_set,
            signing_key_identity=(
                expected.signing_key_identity
            ),
        )
    )

    assert resolved is expected


def test_unknown_identity_returns_none() -> None:
    binding_set = create_binding_set(
        size=3,
    )
    unknown = binding(4)

    resolved = (
        resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding(
            binding_set=binding_set,
            signing_key_identity=(
                unknown.signing_key_identity
            ),
        )
    )

    assert resolved is None


def test_same_key_id_with_wrong_fingerprint_returns_none() -> None:
    binding_set = create_binding_set(
        size=3,
    )
    existing = binding_set.bindings[0]
    fingerprint = (
        existing
        .signing_key_identity
        .public_key_fingerprint
    )
    replacement = (
        "0" if fingerprint[0] != "0" else "1"
    )
    changed_identity = replace(
        existing.signing_key_identity,
        public_key_fingerprint=(
            replacement + fingerprint[1:]
        ),
    )

    resolved = (
        resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding(
            binding_set=binding_set,
            signing_key_identity=changed_identity,
        )
    )

    assert resolved is None


def test_same_public_key_with_wrong_key_id_returns_none() -> None:
    binding_set = create_binding_set(
        size=3,
    )
    other_label = create_binding(
        scalar=1,
        key_id=(
            "kms://security-admission/"
            "different-key-id"
        ),
    )

    resolved = (
        resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding(
            binding_set=binding_set,
            signing_key_identity=(
                other_label.signing_key_identity
            ),
        )
    )

    assert resolved is None


def test_matching_value_identity_resolves() -> None:
    binding_set = create_binding_set(
        size=3,
    )
    existing = binding_set.bindings[1]
    equal_identity = replace(
        existing.signing_key_identity
    )

    assert (
        equal_identity
        == existing.signing_key_identity
    )
    assert (
        equal_identity
        is not existing.signing_key_identity
    )

    resolved = (
        resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding(
            binding_set=binding_set,
            signing_key_identity=equal_identity,
        )
    )

    assert resolved is existing


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "binding-set",
        b"binding-set",
        1,
        True,
        (),
    ),
)
def test_binding_set_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="binding_set",
    ):
        resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding(
            binding_set=value,
            signing_key_identity=(
                binding(1).signing_key_identity
            ),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "identity",
        b"identity",
        1,
        True,
        (),
    ),
)
def test_signing_key_identity_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="signing_key_identity",
    ):
        resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding(
            binding_set=create_binding_set(),
            signing_key_identity=value,
        )


def test_resolution_preserves_binding_set() -> None:
    binding_set = create_binding_set(
        size=3,
    )
    bindings = binding_set.bindings
    first = bindings[0]
    second = bindings[1]
    third = bindings[2]

    resolved = (
        resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding(
            binding_set=binding_set,
            signing_key_identity=(
                second.signing_key_identity
            ),
        )
    )

    assert resolved is second
    assert binding_set.bindings is bindings
    assert binding_set.bindings == (
        first,
        second,
        third,
    )


def test_resolution_has_exact_boundary() -> None:
    parameters = inspect.signature(
        resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding
    ).parameters

    assert tuple(parameters) == (
        "binding_set",
        "signing_key_identity",
    )


def test_resolution_does_not_receive_private_key() -> None:
    source = inspect.getsource(
        resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding
    )

    assert "private_key" not in source
    assert "private_bytes" not in source


def test_resolution_does_not_verify_or_decide() -> None:
    source = inspect.getsource(
        resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding
    ).lower()
    forbidden = (
        ".verify",
        "admission_decision",
        "authorization",
        "authority",
        "rejection",
        "classification",
    )

    assert all(
        token not in source
        for token in forbidden
    )
