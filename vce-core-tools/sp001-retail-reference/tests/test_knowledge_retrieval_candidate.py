from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from sp001.contracts.knowledge_retrieval_candidate import (
    KnowledgeRetrievalCandidate,
    KnowledgeRetrievalCandidateSet,
)
from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeRetrievalContext,
)
from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeSourceEffectivePeriod,
)
from sp001.contracts.knowledge_source_identity import (
    KnowledgeSourceIdentity,
)
from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeScopeMode,
    KnowledgeScopeSelection,
    KnowledgeSourceScope,
)
from sp001.contracts.knowledge_source_status import (
    KnowledgeEvidenceStatus,
    KnowledgeLifecycleStatus,
    KnowledgeSourceStatus,
)
from sp001.contracts.knowledge_source_supersession import (
    KnowledgeSourceSupersessionGraph,
)
from sp001.services.knowledge_source_integrity import (
    digest_knowledge_source_content,
)


CONTENT = b"governed planogram bytes"
EVALUATED_AT = datetime(
    2026,
    3,
    15,
    12,
    tzinfo=timezone.utc,
)


def selection(identity: str) -> KnowledgeScopeSelection:
    return KnowledgeScopeSelection(
        mode=KnowledgeScopeMode.EXPLICIT,
        ids=(identity,),
    )


def create_status(
    *,
    source_id: str = "SOURCE-001",
    source_version: str = "v1",
) -> KnowledgeSourceStatus:
    return KnowledgeSourceStatus(
        status_record_id=f"STATUS-{source_id}",
        status_version=1,
        identity=KnowledgeSourceIdentity(
            source_id=source_id,
            source_version=source_version,
            source_content_digest=(
                digest_knowledge_source_content(
                    content=CONTENT,
                )
            ),
        ),
        scope=KnowledgeSourceScope(
            organization_id="ORG-001",
            customer_id="CUSTOMER-001",
            jurisdiction="MX",
            commercial_channel_id="PHYSICAL-STORE",
            document_type=KnowledgeDocumentType.PLANOGRAM,
            point_of_sale_scope=selection("POS-045"),
            department_scope=selection("DPT-DENIM"),
            campaign_id="CAMP-SPRING-2026",
        ),
        lifecycle_status=KnowledgeLifecycleStatus.APPROVED,
        evidence_status=KnowledgeEvidenceStatus.SUPPORTED,
    )


def create_context() -> KnowledgeRetrievalContext:
    return KnowledgeRetrievalContext(
        organization_id="ORG-001",
        customer_id="CUSTOMER-001",
        jurisdiction="MX",
        commercial_channel_id="PHYSICAL-STORE",
        document_type=KnowledgeDocumentType.PLANOGRAM,
        point_of_sale_id="POS-045",
        department_id="DPT-DENIM",
        campaign_id="CAMP-SPRING-2026",
        evaluated_at=EVALUATED_AT,
    )


def create_candidate(
    *,
    candidate_id: str = "CANDIDATE-001",
    source: KnowledgeSourceStatus | None = None,
    content: bytes = CONTENT,
    authority_bindings: tuple = (),
) -> KnowledgeRetrievalCandidate:
    selected_source = source or create_status()

    return KnowledgeRetrievalCandidate(
        candidate_id=candidate_id,
        source_status=selected_source,
        content=content,
        effective_period=KnowledgeSourceEffectivePeriod(
            source_status=selected_source,
            effective_from=datetime(
                2026,
                3,
                1,
                tzinfo=timezone.utc,
            ),
        ),
        authority_bindings=authority_bindings,
    )


def create_set(
    *candidates: KnowledgeRetrievalCandidate,
) -> KnowledgeRetrievalCandidateSet:
    return KnowledgeRetrievalCandidateSet(
        retrieval_context=create_context(),
        candidates=tuple(candidates),
        supersession_graph=KnowledgeSourceSupersessionGraph(
            supersessions=(),
        ),
    )


def test_candidate_preserves_complete_evaluation_input() -> None:
    candidate = create_candidate()

    assert candidate.candidate_id == "CANDIDATE-001"
    assert candidate.content == CONTENT
    assert candidate.authority_bindings == ()
    assert (
        candidate.effective_period.source_status
        is candidate.source_status
    )


@pytest.mark.parametrize(
    "candidate_id",
    ("", " "),
)
def test_candidate_rejects_empty_identity(
    candidate_id: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="candidate_id must not be empty",
    ):
        create_candidate(candidate_id=candidate_id)


def test_candidate_rejects_untyped_source_status() -> None:
    source = create_status()

    with pytest.raises(
        TypeError,
        match="source_status must be a KnowledgeSourceStatus",
    ):
        KnowledgeRetrievalCandidate(
            candidate_id="CANDIDATE-001",
            source_status="source",
            content=CONTENT,
            effective_period=KnowledgeSourceEffectivePeriod(
                source_status=source,
                effective_from=EVALUATED_AT,
            ),
            authority_bindings=(),
        )


def test_candidate_requires_immutable_nonempty_bytes() -> None:
    with pytest.raises(
        TypeError,
        match="content must be immutable bytes",
    ):
        create_candidate(content=bytearray(CONTENT))

    with pytest.raises(
        ValueError,
        match="content must not be empty",
    ):
        create_candidate(content=b"")


def test_period_must_describe_candidate_source() -> None:
    source = create_status()
    other = create_status(source_id="SOURCE-OTHER")

    with pytest.raises(
        ValueError,
        match="effective_period must describe source_status",
    ):
        KnowledgeRetrievalCandidate(
            candidate_id="CANDIDATE-001",
            source_status=source,
            content=CONTENT,
            effective_period=KnowledgeSourceEffectivePeriod(
                source_status=other,
                effective_from=EVALUATED_AT,
            ),
            authority_bindings=(),
        )


def test_candidate_rejects_mutable_authority_collection() -> None:
    with pytest.raises(
        TypeError,
        match="authority_bindings must be an immutable tuple",
    ):
        create_candidate(authority_bindings=[])


def test_candidate_rejects_untyped_authority_binding() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeAuthorityBinding values",
    ):
        create_candidate(
            authority_bindings=("binding",),
        )


def test_candidate_is_immutable() -> None:
    candidate = create_candidate()

    with pytest.raises(FrozenInstanceError):
        candidate.content = b"changed"


def test_empty_candidate_set_is_explicitly_valid() -> None:
    candidate_set = create_set()

    assert candidate_set.candidates == ()


def test_candidate_set_preserves_declared_order() -> None:
    first = create_candidate(
        candidate_id="CANDIDATE-001",
        source=create_status(source_id="SOURCE-001"),
    )
    second = create_candidate(
        candidate_id="CANDIDATE-002",
        source=create_status(source_id="SOURCE-002"),
    )

    candidate_set = create_set(first, second)

    assert candidate_set.candidates == (first, second)


def test_candidate_set_rejects_mutable_collection() -> None:
    with pytest.raises(
        TypeError,
        match="candidates must be an immutable tuple",
    ):
        KnowledgeRetrievalCandidateSet(
            retrieval_context=create_context(),
            candidates=[],
            supersession_graph=(
                KnowledgeSourceSupersessionGraph(
                    supersessions=(),
                )
            ),
        )


def test_candidate_set_rejects_duplicate_candidate_identity() -> None:
    first = create_candidate()
    second = create_candidate(
        candidate_id="CANDIDATE-001",
        source=create_status(source_id="SOURCE-002"),
    )

    with pytest.raises(
        ValueError,
        match="duplicate candidate_id: CANDIDATE-001",
    ):
        create_set(first, second)


def test_candidate_set_rejects_duplicate_source_identity() -> None:
    source = create_status()
    first = create_candidate(
        candidate_id="CANDIDATE-001",
        source=source,
    )
    second = create_candidate(
        candidate_id="CANDIDATE-002",
        source=source,
    )

    with pytest.raises(
        ValueError,
        match="duplicate candidate source identity",
    ):
        create_set(first, second)


def test_candidate_set_rejects_untyped_members() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeRetrievalCandidate values",
    ):
        create_set("candidate")


def test_candidate_set_is_immutable() -> None:
    candidate_set = create_set(
        create_candidate(),
    )

    with pytest.raises(FrozenInstanceError):
        candidate_set.candidates = ()


def test_candidate_set_does_not_claim_ranking_or_retrieval() -> None:
    candidate_set = create_set(
        create_candidate(),
    )

    for attribute in (
        "included_decisions",
        "excluded_decisions",
        "ranking",
        "score",
        "relevance",
        "selected",
        "manifest_digest",
        "answer",
    ):
        assert not hasattr(candidate_set, attribute)
