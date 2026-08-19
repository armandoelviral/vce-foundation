from dataclasses import dataclass

from sp001.services.retail_context_assessment_report import (
    RetailContextAssessmentReport,
)
from sp001.services.retail_context_assessment_report_digest import (
    RetailContextAssessmentReportDigest,
    digest_retail_context_assessment_report,
)
from sp001.services.retail_context_assessment_report_serialization import (
    serialize_retail_context_assessment_report,
)


@dataclass(frozen=True, slots=True)
class RetailContextAssessmentReportArtifact:
    """Immutable report payload and content digest for bounded exchange."""

    payload: str
    digest: RetailContextAssessmentReportDigest
    media_type: str


def build_retail_context_assessment_report_artifact(
    *,
    report: RetailContextAssessmentReport,
) -> RetailContextAssessmentReportArtifact:
    """Package deterministic report content without authenticity claims."""

    if not isinstance(
        report,
        RetailContextAssessmentReport,
    ):
        raise TypeError(
            "report must be a "
            "RetailContextAssessmentReport"
        )

    payload = serialize_retail_context_assessment_report(
        report=report,
    )

    digest = digest_retail_context_assessment_report(
        report=report,
    )

    return RetailContextAssessmentReportArtifact(
        payload=payload,
        digest=digest,
        media_type="application/json",
    )
