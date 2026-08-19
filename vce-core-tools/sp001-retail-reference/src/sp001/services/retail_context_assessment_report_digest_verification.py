import hmac
import re

from sp001.services.retail_context_assessment_report import (
    RetailContextAssessmentReport,
)
from sp001.services.retail_context_assessment_report_digest import (
    RetailContextAssessmentReportDigest,
    digest_retail_context_assessment_report,
)


def verify_retail_context_assessment_report_digest(
    *,
    report: RetailContextAssessmentReport,
    digest: RetailContextAssessmentReportDigest,
) -> bool:
    """Verify content correspondence without asserting authenticity."""

    if not isinstance(
        report,
        RetailContextAssessmentReport,
    ):
        raise TypeError(
            "report must be a "
            "RetailContextAssessmentReport"
        )

    if not isinstance(
        digest,
        RetailContextAssessmentReportDigest,
    ):
        raise TypeError(
            "digest must be a "
            "RetailContextAssessmentReportDigest"
        )

    if digest.algorithm != "SHA-256":
        raise ValueError(
            "digest algorithm must be SHA-256"
        )

    if digest.encoding != "UTF-8":
        raise ValueError(
            "digest encoding must be UTF-8"
        )

    if (
        not isinstance(
            digest.value,
            str,
        )
        or re.fullmatch(
            r"[0-9a-f]{64}",
            digest.value,
        )
        is None
    ):
        raise ValueError(
            "digest value must contain "
            "64 lowercase hexadecimal characters"
        )

    expected = digest_retail_context_assessment_report(
        report=report,
    )

    return hmac.compare_digest(
        expected.value,
        digest.value,
    )
