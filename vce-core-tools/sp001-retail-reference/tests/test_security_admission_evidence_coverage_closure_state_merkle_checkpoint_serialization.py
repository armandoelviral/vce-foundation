import ast
import inspect
import json

import pytest

from sp001.services import (
    security_admission_evidence_coverage_closure_state_merkle_checkpoint_serialization
    as serialization_module,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_projection import (
    create_checkpoint,
)


def serialize(
    checkpoint: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
) -> str:
    return (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=checkpoint,
        )
    )


def test_serialization_matches_exact_canonical_json() -> None:
    checkpoint = create_checkpoint()

    expected = (
        '{"domain":'
        '"SP001-SECURITY-ADMISSION-CLOSURE-STATE-'
        'MERKLE-CHECKPOINT",'
        '"origin":"sp001-security-admission",'
        '"root":{'
        '"algorithm":"SHA-256",'
        '"leaf_count":3,'
        '"tree_hash_profile":"RFC6962",'
        f'"value":"{checkpoint.root.value}"'
        '}}'
    )

    assert serialize(checkpoint) == expected


def test_serialization_round_trips_to_projection() -> None:
    checkpoint = create_checkpoint()
    payload = serialize(checkpoint)

    assert json.loads(payload) == (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=checkpoint,
        )
    )


def test_serialization_is_deterministic() -> None:
    checkpoint = create_checkpoint()

    first = serialize(checkpoint)
    second = serialize(checkpoint)
    third = serialize(checkpoint)

    assert first == second == third


@pytest.mark.parametrize(
    ("origin", "size"),
    (
        ("sp001-security-admission", 1),
        ("retail/security/admission", 2),
        ("urn:sp001:security-admission", 4),
        ("tenant-001", 7),
        ("admisión-segura", 9),
    ),
)
def test_serialization_preserves_checkpoint_values(
    origin: str,
    size: int,
) -> None:
    checkpoint = create_checkpoint(
        origin=origin,
        size=size,
    )
    document = json.loads(serialize(checkpoint))

    assert document["origin"] == origin
    assert document["root"]["leaf_count"] == size
    assert document["root"]["value"] == checkpoint.root.value


def test_unicode_is_not_ascii_escaped() -> None:
    checkpoint = create_checkpoint(
        origin="admisión-segura",
    )
    payload = serialize(checkpoint)

    assert "admisión-segura" in payload
    assert "\\u00f3" not in payload


def test_serialization_contains_no_insignificant_whitespace() -> None:
    payload = serialize(create_checkpoint())

    assert ": " not in payload
    assert ", " not in payload
    assert "\n" not in payload
    assert "\t" not in payload


def test_serialized_keys_are_lexicographically_sorted() -> None:
    payload = serialize(create_checkpoint())

    assert payload.index('"domain"') < payload.index('"origin"')
    assert payload.index('"origin"') < payload.index('"root"')
    assert payload.index('"algorithm"') < payload.index('"leaf_count"')
    assert (
        payload.index('"leaf_count"')
        < payload.index('"tree_hash_profile"')
    )
    assert (
        payload.index('"tree_hash_profile"')
        < payload.index('"value"')
    )


def test_serialization_returns_exact_string_type() -> None:
    payload = serialize(create_checkpoint())

    assert type(payload) is str


def test_serialization_does_not_mutate_checkpoint() -> None:
    checkpoint = create_checkpoint()
    origin = checkpoint.origin
    root = checkpoint.root

    serialize(checkpoint)

    assert checkpoint.origin == origin
    assert checkpoint.root is root


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        "checkpoint",
        {},
        object(),
    ),
)
def test_serialization_requires_nominal_checkpoint(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "checkpoint must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint"
        ),
    ):
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=invalid_value,  # type: ignore[arg-type]
        )


def test_json_dump_configuration_is_exact() -> None:
    source = inspect.getsource(
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint
    )
    tree = ast.parse(source)

    calls = [
        node
        for node in ast.walk(tree)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "json"
            and node.func.attr == "dumps"
        )
    ]

    assert len(calls) == 1

    keywords = {
        keyword.arg: ast.literal_eval(keyword.value)
        for keyword in calls[0].keywords
    }

    assert keywords == {
        "sort_keys": True,
        "separators": (",", ":"),
        "ensure_ascii": False,
        "allow_nan": False,
    }


def test_serialization_has_no_signing_execution() -> None:
    source = inspect.getsource(serialization_module)
    tree = ast.parse(source)

    imported_names = {
        alias.name
        for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }

    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
        )
    }

    assert "cryptography" not in imported_names
    assert "hmac" not in imported_names
    assert "sign" not in called_names
    assert "verify" not in called_names


def test_serialization_adds_no_signature_or_time_claim() -> None:
    payload = serialize(create_checkpoint())

    assert '"signature"' not in payload
    assert '"key_id"' not in payload
    assert '"timestamp"' not in payload
    assert '"created_at"' not in payload
    assert '"issued_at"' not in payload
