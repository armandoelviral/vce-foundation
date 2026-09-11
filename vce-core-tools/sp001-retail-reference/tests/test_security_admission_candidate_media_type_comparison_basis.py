from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timezone
import ast
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
)
from sp001.contracts.security_admission_candidate_declared_media_type import (
    SecurityAdmissionCandidateDeclaredMediaType,
)
from sp001.contracts.security_admission_candidate_detected_media_type_observation import (
    SecurityAdmissionCandidateDetectedMediaTypeObservation,
)
from sp001.contracts.security_admission_candidate_identity import (
    SecurityAdmissionCandidateIdentity,
)
from sp001.contracts.security_admission_candidate_media_type_comparison_basis import (
    SecurityAdmissionCandidateMediaTypeComparisonBasis,
)
from sp001.contracts.security_admission_candidate_metadata_identity import (
    SecurityAdmissionCandidateMetadataIdentity,
)
from sp001.contracts.security_admission_metadata_verification_procedure_identity import (
    SecurityAdmissionMetadataVerificationProcedureIdentity,
)


def create_digest(value: str) -> KnowledgeContentDigest:
    return KnowledgeContentDigest(
        algorithm="SHA-256",
        value=value,
    )


def create_candidate() -> SecurityAdmissionCandidateIdentity:
    return SecurityAdmissionCandidateIdentity(
        candidate_id="candidate-001",
        candidate_version=1,
        customer_id="customer-001",
        content_digest=create_digest("0" * 64),
    )


def create_declaration() -> SecurityAdmissionCandidateDeclaredMediaType:
    metadata = SecurityAdmissionCandidateMetadataIdentity(
        candidate_identity=create_candidate(),
        metadata_schema_id="admission-metadata",
        metadata_schema_version=1,
        metadata_digest=create_digest("1" * 64),
    )
    return SecurityAdmissionCandidateDeclaredMediaType(
        metadata_identity=metadata,
        declared_media_type="IMAGE/JPEG",
    )


def create_detection() -> (
    SecurityAdmissionCandidateDetectedMediaTypeObservation
):
    procedure = SecurityAdmissionMetadataVerificationProcedureIdentity(
        verification_procedure_id="procedure-001",
        verifier_id="metadata-verifier",
        verifier_version="v1",
        configuration_digest=create_digest("2" * 64),
    )
    return SecurityAdmissionCandidateDetectedMediaTypeObservation(
        observation_id="observation-001",
        observation_version=1,
        candidate_identity=create_candidate(),
        verification_procedure_identity=procedure,
        detected_media_type="image/jpeg",
        observed_at=datetime(2026, 9, 11, tzinfo=timezone.utc),
    )


def create_basis() -> SecurityAdmissionCandidateMediaTypeComparisonBasis:
    return SecurityAdmissionCandidateMediaTypeComparisonBasis(
        declared_media_type=create_declaration(),
        detected_media_type_observation=create_detection(),
        comparison_scheme_id="media-type-comparison",
        comparison_scheme_version=1,
    )


def test_media_type_comparison_basis_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionCandidateMediaTypeComparisonBasis
        )
    ) == (
        "declared_media_type",
        "detected_media_type_observation",
        "comparison_scheme_id",
        "comparison_scheme_version",
    )


def test_media_type_comparison_basis_is_immutable() -> None:
    basis = create_basis()

    with pytest.raises(FrozenInstanceError):
        basis.comparison_scheme_version = 2  # type: ignore[misc]


def test_media_type_comparison_basis_uses_slots() -> None:
    assert not hasattr(create_basis(), "__dict__")


def test_declared_media_type_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "declared_media_type must be a "
            "SecurityAdmissionCandidateDeclaredMediaType"
        ),
    ):
        replace(
            create_basis(),
            declared_media_type=object(),  # type: ignore[arg-type]
        )


def test_exact_declaration_reference_is_preserved() -> None:
    declaration = create_declaration()
    basis = replace(
        create_basis(),
        declared_media_type=declaration,
    )

    assert basis.declared_media_type is declaration


def test_detected_observation_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "detected_media_type_observation must be a "
            "SecurityAdmissionCandidateDetectedMediaTypeObservation"
        ),
    ):
        replace(
            create_basis(),
            detected_media_type_observation=object(),  # type: ignore[arg-type]
        )


def test_exact_detection_reference_is_preserved() -> None:
    detection = create_detection()
    basis = replace(
        create_basis(),
        detected_media_type_observation=detection,
    )

    assert basis.detected_media_type_observation is detection


def test_reconstructed_candidate_identity_is_compatible() -> None:
    declaration = create_declaration()
    detection = create_detection()

    assert (
        declaration.metadata_identity.candidate_identity
        == detection.candidate_identity
    )
    assert (
        declaration.metadata_identity.candidate_identity
        is not detection.candidate_identity
    )

    basis = SecurityAdmissionCandidateMediaTypeComparisonBasis(
        declared_media_type=declaration,
        detected_media_type_observation=detection,
        comparison_scheme_id="media-type-comparison",
        comparison_scheme_version=1,
    )

    assert basis.declared_media_type is declaration
    assert basis.detected_media_type_observation is detection


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("candidate_id", "candidate-002"),
        ("candidate_version", 2),
        ("customer_id", "customer-002"),
        ("content_digest", create_digest("f" * 64)),
    ],
)
def test_incompatible_candidate_identity_is_rejected(
    field_name: str,
    value: object,
) -> None:
    basis = create_basis()
    incompatible_candidate = replace(
        basis.detected_media_type_observation.candidate_identity,
        **{field_name: value},
    )
    incompatible_detection = replace(
        basis.detected_media_type_observation,
        candidate_identity=incompatible_candidate,
    )

    with pytest.raises(
        ValueError,
        match=(
            "declared and detected media types must reference "
            "the same candidate_identity"
        ),
    ):
        replace(
            basis,
            detected_media_type_observation=incompatible_detection,
        )


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_comparison_scheme_id_requires_string(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="comparison_scheme_id must be a string",
    ):
        replace(
            create_basis(),
            comparison_scheme_id=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", " ", "\t", "\n"])
def test_comparison_scheme_id_must_not_be_blank(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="comparison_scheme_id must not be blank",
    ):
        replace(
            create_basis(),
            comparison_scheme_id=value,
        )


def test_comparison_scheme_id_is_preserved_literally() -> None:
    value = " Media-Comparison-Scheme "
    basis = replace(
        create_basis(),
        comparison_scheme_id=value,
    )

    assert basis.comparison_scheme_id == value


@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_comparison_scheme_version_requires_strict_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="comparison_scheme_version must be an integer",
    ):
        replace(
            create_basis(),
            comparison_scheme_version=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", [0, -1, -(10**30)])
def test_comparison_scheme_version_must_be_positive(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="comparison_scheme_version must be positive",
    ):
        replace(
            create_basis(),
            comparison_scheme_version=value,
        )


def test_reconstructed_equal_basis_has_value_equality() -> None:
    original = create_basis()
    reconstructed = SecurityAdmissionCandidateMediaTypeComparisonBasis(
        declared_media_type=create_declaration(),
        detected_media_type_observation=create_detection(),
        comparison_scheme_id="media-type-comparison",
        comparison_scheme_version=1,
    )

    assert reconstructed == original
    assert reconstructed is not original


def test_every_field_participates_in_basis_identity() -> None:
    basis = create_basis()

    assert replace(
        basis,
        declared_media_type=replace(
            basis.declared_media_type,
            declared_media_type="application/json",
        ),
    ) != basis
    assert replace(
        basis,
        detected_media_type_observation=replace(
            basis.detected_media_type_observation,
            detected_media_type="application/json",
        ),
    ) != basis
    assert replace(
        basis,
        comparison_scheme_id="other-scheme",
    ) != basis
    assert replace(
        basis,
        comparison_scheme_version=2,
    ) != basis


def test_unequal_media_values_remain_admissible_inputs() -> None:
    basis = create_basis()

    assert (
        basis.declared_media_type.declared_media_type
        != basis.detected_media_type_observation.detected_media_type
    )


def test_result_and_admission_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateMediaTypeComparisonBasis
        )
    }

    assert names.isdisjoint(
        {
            "match_status",
            "mismatch_reason",
            "matches",
            "normalized_declared_media_type",
            "normalized_detected_media_type",
            "compared_at",
            "status",
            "decision",
            "reason",
            "authorized",
            "rejected",
            "suspicious",
            "quarantine",
            "retention",
        }
    )


def test_contract_performs_no_media_value_comparison() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateMediaTypeComparisonBasis
    )
    assert module is not None
    source = inspect.getsource(module)
    tree = ast.parse(source)
    accessed_attributes = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
    }

    assert "detected_media_type" not in accessed_attributes
    assert "casefold(" not in source
    assert "lower(" not in source
    assert "upper(" not in source


def test_contract_imports_no_comparison_or_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateMediaTypeComparisonBasis
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    roots.update(
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.module is not None
    )

    assert roots.isdisjoint(
        {
            "re",
            "mimetypes",
            "magic",
            "os",
            "pathlib",
            "subprocess",
            "sqlite3",
            "requests",
            "httpx",
            "urllib",
            "openai",
            "notion_client",
        }
    )


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateMediaTypeComparisonBasis
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
