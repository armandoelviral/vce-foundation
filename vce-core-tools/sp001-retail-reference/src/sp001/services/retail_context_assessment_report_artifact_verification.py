import hashlib
import hmac
import json
import re

from sp001.services.retail_context_assessment_report_artifact import (
    RetailContextAssessmentReportArtifact,
)
from sp001.services.retail_context_assessment_report_digest import (
    RetailContextAssessmentReportDigest,
)


def verify_retail_context_assessment_report_artifact(
    *,
    artifact: RetailContextAssessmentReportArtifact,
) -> bool:
    """Verify received JSON bytes without asserting report authenticity."""

    if not isinstance(
        artifact,
        RetailContextAssessmentReportArtifact,
    ):
        raise TypeError(
            "artifact must be a "
            "RetailContextAssessmentReportArtifact"
        )

    if artifact.media_type != "application/json":
        raise ValueError(
            "artifact media_type must be application/json"
        )

    if not isinstance(
        artifact.payload,
        str,
    ):
        raise TypeError(
            "artifact payload must be a string"
        )

    if not artifact.payload.strip():
        raise ValueError(
            "artifact payload must not be empty"
        )

    try:
        document = json.loads(
            artifact.payload,
        )
    except (
        json.JSONDecodeError,
        UnicodeError,
    ) as error:
        raise ValueError(
            "artifact payload must contain valid JSON"
        ) from error

    if not isinstance(
        document,
        dict,
    ):
        raise ValueError(
            "artifact payload must contain a JSON object"
        )

    digest = artifact.digest

    if not isinstance(
        digest,
        RetailContextAssessmentReportDigest,
    ):
        raise TypeError(
            "artifact digest must be a "
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

    expected = hashlib.sha256(
        artifact.payload.encode(
            "utf-8",
        )
    ).hexdigest()

    return hmac.compare_digest(
        expected,
        digest.value,
    )
