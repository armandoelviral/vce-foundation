from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.evidence_file_expectation import EvidenceFileExpectation
from sp001.infrastructure.evidence_file_comparison import (
    EvidenceFileComparison, EvidenceFileComparisonStatus,
)
from sp001.services.retail_rule_evaluation_report import RetailRuleEvaluationReport


class UncheckedEvidenceStatus(StrEnum):
    EXPECTATION_MISSING = "EXPECTATION_MISSING"
    NOT_CHECKED = "NOT_CHECKED"


@dataclass(frozen=True, slots=True)
class RetailReportEvidenceReference:
    evidence_id: str
    expectation: EvidenceFileExpectation | None
    comparison: EvidenceFileComparison | None

    @property
    def status(self):
        if self.comparison is not None:
            return self.comparison.status
        if self.expectation is None:
            return UncheckedEvidenceStatus.EXPECTATION_MISSING
        return UncheckedEvidenceStatus.NOT_CHECKED


@dataclass(frozen=True, slots=True)
class RetailReportEvidenceComparison:
    """Supplied byte observations; does not change evaluations or grant authority."""

    report: RetailRuleEvaluationReport
    references: tuple[RetailReportEvidenceReference, ...]


def bind_retail_report_evidence_comparisons(
    *, report: RetailRuleEvaluationReport,
    expectations: tuple[EvidenceFileExpectation, ...],
    comparisons: tuple[EvidenceFileComparison, ...],
) -> RetailReportEvidenceComparison:
    """Bind supplied results by explicit source identity, without filesystem reads.

    Report evidence IDs are opaque and unversioned. Multiple versions under one
    ID are therefore rejected rather than implicitly selecting a version.
    """
    if type(report) is not RetailRuleEvaluationReport:
        raise TypeError("report must be a RetailRuleEvaluationReport")
    if type(expectations) is not tuple or type(comparisons) is not tuple:
        raise TypeError("expectations and comparisons must be tuples")

    evidence_ids = dict.fromkeys(
        evidence_id
        for evaluation in report.evaluations
        for evidence_id in evaluation.observation.evidence_ids
    )
    for relation in report.relations:
        for evidence_id in relation.intervention_evidence_ids:
            evidence_ids.setdefault(evidence_id, None)

    by_id = {}
    for expectation in expectations:
        if type(expectation) is not EvidenceFileExpectation:
            raise TypeError("invalid expectation")
        evidence_id = expectation.identity.source_id
        if evidence_id not in evidence_ids:
            raise ValueError("expectation is outside the report")
        if evidence_id in by_id:
            raise ValueError("duplicate or ambiguous evidence identity")
        by_id[evidence_id] = expectation

    observed = {}
    for comparison in comparisons:
        if type(comparison) is not EvidenceFileComparison:
            raise TypeError("invalid comparison")
        if type(comparison.expectation) is not EvidenceFileExpectation:
            raise TypeError("invalid comparison expectation")
        evidence_id = comparison.expectation.identity.source_id
        if evidence_id not in by_id:
            raise ValueError("comparison has no declared report expectation")
        if comparison.expectation != by_id[evidence_id]:
            raise ValueError("comparison expectation differs")
        if evidence_id in observed:
            raise ValueError("duplicate comparison")
        if type(comparison.status) is not EvidenceFileComparisonStatus:
            raise TypeError("invalid comparison status")

        length = comparison.observed_byte_length
        digest = comparison.observed_digest
        if comparison.status in (
            EvidenceFileComparisonStatus.MATCH,
            EvidenceFileComparisonStatus.DIFFERENT,
        ):
            if type(length) is not int or length < 0:
                raise ValueError("completed comparison requires observed length")
            from sp001.contracts.knowledge_source_identity import KnowledgeContentDigest
            if length == 0:
                if digest is not None:
                    raise ValueError("empty observation must not contain a digest")
            elif type(digest) is not KnowledgeContentDigest:
                raise TypeError("nonempty observation requires a digest")
            matches = (
                length == comparison.expectation.byte_length
                and digest == comparison.expectation.identity.source_content_digest
            )
            if matches != (
                comparison.status is EvidenceFileComparisonStatus.MATCH
            ):
                raise ValueError("comparison status contradicts observed metadata")
        elif length is not None or digest is not None:
            raise ValueError("incomplete comparison must not expose partial metadata")
        observed[evidence_id] = comparison

    return RetailReportEvidenceComparison(
        report=report,
        references=tuple(
            RetailReportEvidenceReference(
                evidence_id=evidence_id,
                expectation=by_id.get(evidence_id),
                comparison=observed.get(evidence_id),
            )
            for evidence_id in evidence_ids
        ),
    )
