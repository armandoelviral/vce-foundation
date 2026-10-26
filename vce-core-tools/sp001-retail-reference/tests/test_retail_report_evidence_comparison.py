from dataclasses import replace

import pytest

import test_retail_rule_evaluation_serialization as setup

from sp001.contracts.evidence_file_expectation import EvidenceFileExpectation
from sp001.contracts.knowledge_source_identity import KnowledgeSourceIdentity
from sp001.infrastructure.evidence_file_comparison import (
    compare_evidence_file, EvidenceFileComparisonStatus as Status,
)
from sp001.services.knowledge_source_integrity import digest_knowledge_source_content
from sp001.services.retail_report_evidence_comparison import (
    bind_retail_report_evidence_comparisons as bind,
    UncheckedEvidenceStatus as Unchecked,
)


def expectation(evidence_id="EVIDENCE-1", version="1"):
    return EvidenceFileExpectation(
        KnowledgeSourceIdentity(
            evidence_id, version,
            digest_knowledge_source_content(content=b"original"),
        ),
        len(b"original"),
    )


def test_preserves_original_report_and_marks_missing_expectation():
    report = setup.make_report()
    result = bind(report=report, expectations=(), comparisons=())
    assert result.report is report
    assert len(result.references) == 1
    assert result.references[0].evidence_id == "EVIDENCE-1"
    assert result.references[0].status is Unchecked.EXPECTATION_MISSING


def test_expectation_does_not_imply_a_completed_check():
    expected = expectation()
    result = bind(
        report=setup.make_report(), expectations=(expected,), comparisons=(),
    )
    reference = result.references[0]
    assert reference.expectation is expected
    assert reference.comparison is None
    assert reference.status is Unchecked.NOT_CHECKED


@pytest.mark.parametrize("content,status", [
    (b"original", Status.MATCH),
    (b"modified", Status.DIFFERENT),
    (None, Status.NOT_FOUND),
])
def test_binds_actual_file_observation_without_changing_evaluation(
    tmp_path, content, status,
):
    report = setup.make_report()
    expected = expectation()
    path = tmp_path / "evidence.bin"
    if content is not None:
        path.write_bytes(content)
    comparison = compare_evidence_file(
        expectation=expected, path=path, max_bytes=100,
    )
    result = bind(
        report=report, expectations=(expected,), comparisons=(comparison,),
    )
    assert result.report is report
    assert result.report.evaluations[0] is report.evaluations[0]
    assert result.references[0].comparison is comparison
    assert result.references[0].status is status


def test_rejects_ambiguous_versions_in_unversioned_report_reference():
    with pytest.raises(ValueError, match="ambiguous"):
        bind(
            report=setup.make_report(),
            expectations=(expectation(), expectation(version="2")),
            comparisons=(),
        )


def test_rejects_expectations_outside_report():
    with pytest.raises(ValueError, match="outside"):
        bind(
            report=setup.make_report(),
            expectations=(expectation("OTHER"),), comparisons=(),
        )


def test_comparison_must_match_exact_expected_version(tmp_path):
    path = tmp_path / "file"
    path.write_bytes(b"original")
    comparison = compare_evidence_file(
        expectation=expectation(version="2"), path=path, max_bytes=100,
    )
    with pytest.raises(ValueError, match="differs"):
        bind(
            report=setup.make_report(),
            expectations=(expectation(),), comparisons=(comparison,),
        )


def test_rejects_comparison_without_expectation(tmp_path):
    comparison = compare_evidence_file(
        expectation=expectation(), path=tmp_path / "missing", max_bytes=100,
    )
    with pytest.raises(ValueError, match="no declared"):
        bind(report=setup.make_report(), expectations=(), comparisons=(comparison,))


def test_rejects_duplicate_observations(tmp_path):
    expected = expectation()
    comparison = compare_evidence_file(
        expectation=expected, path=tmp_path / "missing", max_bytes=100,
    )
    with pytest.raises(ValueError, match="duplicate comparison"):
        bind(
            report=setup.make_report(), expectations=(expected,),
            comparisons=(comparison, comparison),
        )


def test_rejects_status_contradicting_observed_metadata(tmp_path):
    path = tmp_path / "file"
    path.write_bytes(b"modified")
    expected = expectation()
    comparison = compare_evidence_file(
        expectation=expected, path=path, max_bytes=100,
    )
    with pytest.raises(ValueError, match="contradicts"):
        bind(
            report=setup.make_report(), expectations=(expected,),
            comparisons=(replace(comparison, status=Status.MATCH),),
        )
