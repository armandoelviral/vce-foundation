from dataclasses import dataclass
import hashlib

from sp001.services.retail_context_assessment_report import (
    RetailContextAssessmentReport,
)
from sp001.services.retail_context_assessment_report_serialization import (
    serialize_retail_context_assessment_report,
)


@dataclass(frozen=True, slots=True)
class RetailContextAssessmentReportDigest:
    """Immutable SHA-256 content identity, without authenticity claims."""

    algorithm: str
    encoding: str
    value: str


def digest_retail_context_assessment_report(
    *,
    report: RetailContextAssessmentReport,
) -> RetailContextAssessmentReportDigest:
    """Digest deterministic report JSON encoded as UTF-8 bytes."""

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

    value = hashlib.sha256(
        payload.encode(
            "utf-8",
        )
    ).hexdigest()

    return RetailContextAssessmentReportDigest(
        algorithm="SHA-256",
        encoding="UTF-8",
        value=value,
    )
