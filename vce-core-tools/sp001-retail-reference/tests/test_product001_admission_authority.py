"""Known PRODUCT-001 decision-authority boundary defect."""

from dataclasses import replace

import pytest

from product001_admission_fixtures import make_valid_admission_case
from test_knowledge_source_retrieval import evaluate
from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
)
from sp001.services.product001_planogram_admission import (
    generate_admitted_planogram_expected_state,
)


def test_forged_included_decision_cannot_authorize_expected_state():
    case = make_valid_admission_case()

    excluded = evaluate(
        source=case.decision.source_status,
        content=b"tampered planogram content",
    )
    assert excluded.decision_status is KnowledgeRetrievalDecisionStatus.EXCLUDED

    forged = replace(
        excluded,
        decision_status=KnowledgeRetrievalDecisionStatus.INCLUDED,
        content_bytes_match_digest=True,
        exclusion_reasons=(),
    )

    assert forged.decision_status is KnowledgeRetrievalDecisionStatus.INCLUDED

    with pytest.raises(ValueError, match="(?i)authority|untrusted|issuer"):
        generate_admitted_planogram_expected_state(
            expected_state_id="PRODUCT-001-AUTHORITY-REGRESSION",
            expected_state_version=1,
            rule=case.rule,
            snapshot=case.snapshot,
            retrieval_decision=forged,
            provenance_bindings=case.bindings,
            planogram_dimension_ids=case.planogram_dimension_ids,
        )
