from dataclasses import asdict
import json

from sp001.services.retail_context_assessment_report import (
    RetailContextAssessmentReport,
)


def serialize_retail_context_assessment_report(
    *,
    report: RetailContextAssessmentReport,
) -> str:
    """Serialize one sanitized retail report using deterministic JSON."""

    if not isinstance(
        report,
        RetailContextAssessmentReport,
    ):
        raise TypeError(
            "report must be a "
            "RetailContextAssessmentReport"
        )

    document = asdict(
        report,
    )

    return json.dumps(
        document,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
        ensure_ascii=False,
        allow_nan=False,
    )
