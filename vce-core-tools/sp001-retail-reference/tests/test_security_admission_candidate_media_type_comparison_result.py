from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta, timezone
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
from sp001.contracts.security_admission_candidate_media_type_comparison_result import (
    SecurityAdmissionCandidateMediaTypeComparisonResult,
    SecurityAdmissionMediaTypeComparisonStatus,
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


def create_basis() -> SecurityAdmissionCandidateMediaTypeComparisonBasis:
    candidate = create_candidate()
    metadata = SecurityAdmissionCandidateMetadataIdentity(
        candidate_identity=candidate,
        metadata_schema_id="admission-metadata",
        metadata_schema_version=1,
        metadata_digest=create_digest("1" * 64),
    )
    declaration = SecurityAdmissionCandidateDeclaredMediaType(
        metadata_identity=metadata,
        declared_media_type="IMAGE/JPEG",
    )
    procedure = SecurityAdmissionMetadataVerificationProcedureIdentity(
        verification_procedure_id="procedure-001",
        verifier_id="metadata-verifier",
        verifier_version="v1",
        configuration_digest=create_digest("2" * 64),
    )
    detection = (
        SecurityAdmissionCandidateDetectedMediaTypeObservation(
            observation_id="observation-001",
            observation_version=1,
            candidate_identity=create_candidate(),
            verification_procedure_identity=procedure,
            detected_media_type="image/jpeg",
            observed_at=datetime(
                2026,
                9,
                11,
                tzinfo=timezone.utc,
            ),
        )
    )
    return SecurityAdmissionCandidateMediaTypeComparisonBasis(
        declared_media_type=declaration,
        detected_media_type_observation=detection,
        comparison_scheme_id="media-type-comparison",
        comparison_scheme_version=1,
    )


def create_result() -> (
    SecurityAdmissionCandidateMediaTypeComparisonResult
):
    return SecurityAdmissionCandidateMediaTypeComparisonResult(
        result_id="result-001",
        result_version=1,
        comparison_basis=create_basis(),
        match_status=(
            SecurityAdmissionMediaTypeComparisonStatus.MATCHES
        ),
        compared_at=datetime(2026, 9, 11, tzinfo=timezone.utc),
    )


def test_media_type_comparison_status_is_exact_and_closed() -> None:
    assert tuple(
        SecurityAdmissionMediaTypeComparisonStatus
    ) == (
        SecurityAdmissionMediaTypeComparisonStatus.MATCHES,
        SecurityAdmissionMediaTypeComparisonStatus.DOES_NOT_MATCH,
    )
    assert tuple(
        member.value
        for member in SecurityAdmissionMediaTypeComparisonStatus
    ) == (
        "MATCHES",
        "DOES_NOT_MATCH",
    )


def test_media_type_comparison_result_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionCandidateMediaTypeComparisonResult
        )
    ) == (
        "result_id",
        "result_version",
        "comparison_basis",
        "match_status",
        "compared_at",
    )


def test_media_type_comparison_result_is_immutable() -> None:
    result = create_result()

    with pytest.raises(FrozenInstanceError):
        result.result_version = 2  # type: ignore[misc]


def test_media_type_comparison_result_uses_slots() -> None:
    assert not hasattr(create_result(), "__dict__")


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_result_id_requires_string(value: object) -> None:
    with pytest.raises(
        TypeError,
        match="result_id must be a string",
    ):
        replace(
            create_result(),
            result_id=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", " ", "\t", "\n"])
def test_result_id_must_not_be_blank(value: str) -> None:
    with pytest.raises(
        ValueError,
        match="result_id must not be blank",
    ):
        replace(create_result(), result_id=value)


def test_result_id_is_preserved_literally() -> None:
    value = " Result-001 "
    result = replace(create_result(), result_id=value)

    assert result.result_id == value


@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_result_version_requires_strict_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="result_version must be an integer",
    ):
        replace(
            create_result(),
            result_version=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", [0, -1, -(10**30)])
def test_result_version_must_be_positive(value: int) -> None:
    with pytest.raises(
        ValueError,
        match="result_version must be positive",
    ):
        replace(create_result(), result_version=value)


def test_comparison_basis_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "comparison_basis must be a "
            "SecurityAdmissionCandidateMediaTypeComparisonBasis"
        ),
    ):
        replace(
            create_result(),
            comparison_basis=object(),  # type: ignore[arg-type]
        )


def test_exact_comparison_basis_reference_is_preserved() -> None:
    basis = create_basis()
    result = replace(create_result(), comparison_basis=basis)

    assert result.comparison_basis is basis


@pytest.mark.parametrize(
    "value",
    [None, "MATCHES", "DOES_NOT_MATCH", object()],
)
def test_match_status_requires_exact_enum(value: object) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "match_status must be a "
            "SecurityAdmissionMediaTypeComparisonStatus"
        ),
    ):
        replace(
            create_result(),
            match_status=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "status",
    list(SecurityAdmissionMediaTypeComparisonStatus),
)
def test_both_conclusive_statuses_are_accepted(
    status: SecurityAdmissionMediaTypeComparisonStatus,
) -> None:
    result = replace(create_result(), match_status=status)

    assert result.match_status is status


@pytest.mark.parametrize("value", [None, "2026-09-11", 1, object()])
def test_compared_at_requires_datetime(value: object) -> None:
    with pytest.raises(
        TypeError,
        match="compared_at must be a datetime",
    ):
        replace(
            create_result(),
            compared_at=value,  # type: ignore[arg-type]
        )


def test_compared_at_must_be_timezone_aware() -> None:
    with pytest.raises(
        ValueError,
        match="compared_at must be timezone-aware",
    ):
        replace(
            create_result(),
            compared_at=datetime(2026, 9, 11),
        )


def test_exact_compared_at_reference_is_preserved() -> None:
    compared_at = datetime(
        2026,
        9,
        11,
        4,
        30,
        tzinfo=timezone(timedelta(hours=-6)),
    )
    result = replace(create_result(), compared_at=compared_at)

    assert result.compared_at is compared_at


def test_reconstructed_equal_result_has_value_equality() -> None:
    original = create_result()
    reconstructed = (
        SecurityAdmissionCandidateMediaTypeComparisonResult(
            result_id="result-001",
            result_version=1,
            comparison_basis=create_basis(),
            match_status=(
                SecurityAdmissionMediaTypeComparisonStatus.MATCHES
            ),
            compared_at=datetime(
                2026,
                9,
                11,
                tzinfo=timezone.utc,
            ),
        )
    )

    assert reconstructed == original
    assert reconstructed is not original


def test_every_field_participates_in_result_identity() -> None:
    result = create_result()

    assert replace(result, result_id="result-002") != result
    assert replace(result, result_version=2) != result
    assert replace(
        result,
        comparison_basis=replace(
            result.comparison_basis,
            comparison_scheme_version=2,
        ),
    ) != result
    assert replace(
        result,
        match_status=(
            SecurityAdmissionMediaTypeComparisonStatus.DOES_NOT_MATCH
        ),
    ) != result
    assert replace(
        result,
        compared_at=datetime(2026, 9, 12, tzinfo=timezone.utc),
    ) != result


def test_indeterminate_and_admission_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateMediaTypeComparisonResult
        )
    }

    assert names.isdisjoint(
        {
            "mismatch_reason",
            "indeterminacy_reason",
            "normalized_declared_media_type",
            "normalized_detected_media_type",
            "status",
            "decision",
            "authorized",
            "rejected",
            "malformed",
            "unsupported",
            "suspicious",
            "quarantine",
            "retention",
        }
    )


def test_contract_performs_no_media_value_comparison() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateMediaTypeComparisonResult
    )
    assert module is not None
    source = inspect.getsource(module)

    assert ".declared_media_type" not in source
    assert ".detected_media_type" not in source
    assert "casefold(" not in source
    assert "lower(" not in source
    assert "upper(" not in source


def test_contract_imports_no_comparison_or_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateMediaTypeComparisonResult
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
        SecurityAdmissionCandidateMediaTypeComparisonResult
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
