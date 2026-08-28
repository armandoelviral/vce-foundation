from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import hashlib

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
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
    KnowledgeSourceSupersession,
    KnowledgeSourceSupersessionGraph,
)
from sp001.contracts.retail_process_actor import (
    ActorType,
    RetailProcessActor,
)
from sp001.contracts.retail_process_role import (
    RetailProcessRole,
)


DECLARED_AT = datetime(
    2026,
    8,
    28,
    tzinfo=timezone.utc,
)


def create_source(
    *,
    source_id: str,
    source_version: str,
    customer_id: str = "BRAND-CASUAL-X",
    document_type: KnowledgeDocumentType = (
        KnowledgeDocumentType.PLANOGRAM
    ),
) -> KnowledgeSourceStatus:
    digest = hashlib.sha256(
        (
            source_id
            + ":"
            + source_version
        ).encode(
            "utf-8",
        )
    ).hexdigest()

    return KnowledgeSourceStatus(
        status_record_id=f"STATUS-{source_id}-{source_version}",
        status_version=1,
        identity=KnowledgeSourceIdentity(
            source_id=source_id,
            source_version=source_version,
            source_content_digest=KnowledgeContentDigest(
                algorithm="SHA-256",
                value=digest,
            ),
        ),
        scope=KnowledgeSourceScope(
            organization_id="RETAIL-GROUP-GLOBAL",
            customer_id=customer_id,
            jurisdiction="MX",
            commercial_channel_id="PHYSICAL_STORE",
            document_type=document_type,
            point_of_sale_scope=KnowledgeScopeSelection(
                mode=KnowledgeScopeMode.ALL,
                ids=(),
            ),
            department_scope=KnowledgeScopeSelection(
                mode=KnowledgeScopeMode.ALL,
                ids=(),
            ),
        ),
        lifecycle_status=KnowledgeLifecycleStatus.APPROVED,
        evidence_status=KnowledgeEvidenceStatus.SUPPORTED,
    )


def create_actor(
    *,
    customer_id: str = "BRAND-CASUAL-X",
    actor_type: ActorType = ActorType.HUMAN,
) -> RetailProcessActor:
    return RetailProcessActor(
        actor_id="ACTOR-VM-DIRECTOR",
        customer_id=customer_id,
        actor_type=actor_type,
        organization_id="RETAIL-GROUP-GLOBAL",
        role=RetailProcessRole(
            role_id="ROLE-VM-DIRECTOR",
            customer_id=customer_id,
            role_name="VM_DIRECTOR",
        ),
    )


def create_supersession(
    *,
    supersession_id: str = "SUPERSESSION-001",
    predecessor: KnowledgeSourceStatus | None = None,
    successor: KnowledgeSourceStatus | None = None,
    declared_by: RetailProcessActor | None = None,
    declaration_evidence_ids: tuple[str, ...] = (
        "SUPERSESSION-EVIDENCE-001",
    ),
    declared_at: datetime = DECLARED_AT,
) -> KnowledgeSourceSupersession:
    return KnowledgeSourceSupersession(
        supersession_id=supersession_id,
        supersession_version=1,
        predecessor_source_status=(
            predecessor
            if predecessor is not None
            else create_source(
                source_id="POG-2025-DENIM-099",
                source_version="legacy",
            )
        ),
        successor_source_status=(
            successor
            if successor is not None
            else create_source(
                source_id="POG-2026-DENIM-012",
                source_version="current",
            )
        ),
        declaration_evidence_ids=(
            declaration_evidence_ids
        ),
        declared_by=(
            declared_by
            if declared_by is not None
            else create_actor()
        ),
        declared_at=declared_at,
    )


def test_supersession_preserves_explicit_direction() -> None:
    supersession = create_supersession()

    assert (
        supersession.predecessor_source_status.identity.source_id
        == "POG-2025-DENIM-099"
    )
    assert (
        supersession.successor_source_status.identity.source_id
        == "POG-2026-DENIM-012"
    )


def test_supersession_preserves_version_and_evidence() -> None:
    supersession = create_supersession()

    assert supersession.supersession_version == 1
    assert supersession.declaration_evidence_ids == (
        "SUPERSESSION-EVIDENCE-001",
    )
    assert supersession.declared_at == DECLARED_AT


@pytest.mark.parametrize(
    "invalid_id",
    (
        "",
        " ",
        None,
        123,
    ),
)
def test_supersession_rejects_empty_identity(
    invalid_id: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="supersession_id must not be empty",
    ):
        KnowledgeSourceSupersession(
            supersession_id=invalid_id,
            supersession_version=1,
            predecessor_source_status=create_source(
                source_id="A",
                source_version="1",
            ),
            successor_source_status=create_source(
                source_id="B",
                source_version="2",
            ),
            declaration_evidence_ids=(
                "EVIDENCE-001",
            ),
            declared_by=create_actor(),
            declared_at=DECLARED_AT,
        )


@pytest.mark.parametrize(
    "invalid_version",
    (
        True,
        0,
        -1,
        1.0,
        "1",
    ),
)
def test_supersession_rejects_invalid_version(
    invalid_version: object,
) -> None:
    supersession = create_supersession()

    with pytest.raises(
        ValueError,
        match=(
            "supersession_version must be "
            "a positive integer"
        ),
    ):
        KnowledgeSourceSupersession(
            supersession_id=supersession.supersession_id,
            supersession_version=invalid_version,
            predecessor_source_status=(
                supersession.predecessor_source_status
            ),
            successor_source_status=(
                supersession.successor_source_status
            ),
            declaration_evidence_ids=(
                supersession.declaration_evidence_ids
            ),
            declared_by=supersession.declared_by,
            declared_at=supersession.declared_at,
        )


def test_source_cannot_supersede_itself() -> None:
    source = create_source(
        source_id="POG-001",
        source_version="v1",
    )

    with pytest.raises(
        ValueError,
        match="source cannot supersede itself",
    ):
        create_supersession(
            predecessor=source,
            successor=source,
        )


def test_supersession_rejects_cross_customer_sources() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "supersession sources must share customer"
        ),
    ):
        create_supersession(
            predecessor=create_source(
                source_id="A",
                source_version="1",
                customer_id="CUSTOMER-A",
            ),
            successor=create_source(
                source_id="B",
                source_version="2",
                customer_id="CUSTOMER-B",
            ),
        )


def test_supersession_rejects_incompatible_document_types() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "supersession sources must share "
            "document_type"
        ),
    ):
        create_supersession(
            predecessor=create_source(
                source_id="A",
                source_version="1",
                document_type=(
                    KnowledgeDocumentType.PLANOGRAM
                ),
            ),
            successor=create_source(
                source_id="B",
                source_version="2",
                document_type=(
                    KnowledgeDocumentType.LOOKBOOK
                ),
            ),
        )


def test_supersession_requires_evidence() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "declaration_evidence_ids "
            "must not be empty"
        ),
    ):
        create_supersession(
            declaration_evidence_ids=(),
        )


def test_supersession_rejects_mutable_evidence() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "declaration_evidence_ids must be "
            "an immutable tuple"
        ),
    ):
        create_supersession(
            declaration_evidence_ids=[
                "EVIDENCE-001",
            ],
        )


def test_supersession_rejects_duplicate_evidence() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "duplicate declaration evidence_id"
        ),
    ):
        create_supersession(
            declaration_evidence_ids=(
                "EVIDENCE-001",
                "EVIDENCE-001",
            ),
        )


def test_system_actor_cannot_declare_supersession() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "SYSTEM actor cannot declare supersession"
        ),
    ):
        create_supersession(
            declared_by=create_actor(
                actor_type=ActorType.SYSTEM,
            ),
        )


def test_cross_customer_actor_cannot_declare_supersession() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "declarer customer must match "
            "supersession customer"
        ),
    ):
        create_supersession(
            declared_by=create_actor(
                customer_id="CUSTOMER-B",
            ),
        )


def test_supersession_requires_timezone_aware_time() -> None:
    with pytest.raises(
        ValueError,
        match="declared_at must be timezone-aware",
    ):
        create_supersession(
            declared_at=datetime(
                2026,
                8,
                28,
            ),
        )


def test_supersession_is_immutable() -> None:
    supersession = create_supersession()

    with pytest.raises(FrozenInstanceError):
        supersession.supersession_version = 2


def test_empty_supersession_graph_is_valid() -> None:
    graph = KnowledgeSourceSupersessionGraph(
        supersessions=(),
    )

    assert graph.supersessions == ()


def test_graph_rejects_mutable_collection() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "supersessions must be an immutable tuple"
        ),
    ):
        KnowledgeSourceSupersessionGraph(
            supersessions=[],
        )


def test_graph_rejects_duplicate_supersession_identity() -> None:
    supersession = create_supersession()

    with pytest.raises(
        ValueError,
        match="duplicate supersession_id",
    ):
        KnowledgeSourceSupersessionGraph(
            supersessions=(
                supersession,
                supersession,
            ),
        )


def test_graph_rejects_duplicate_edge_under_distinct_records() -> None:
    first = create_supersession(
        supersession_id="SUPERSESSION-001",
    )
    second = create_supersession(
        supersession_id="SUPERSESSION-002",
        predecessor=first.predecessor_source_status,
        successor=first.successor_source_status,
    )

    with pytest.raises(
        ValueError,
        match="duplicate supersession edge",
    ):
        KnowledgeSourceSupersessionGraph(
            supersessions=(
                first,
                second,
            ),
        )


def test_graph_rejects_ambiguous_successors() -> None:
    predecessor = create_source(
        source_id="A",
        source_version="1",
    )

    first = create_supersession(
        supersession_id="S-AB",
        predecessor=predecessor,
        successor=create_source(
            source_id="B",
            source_version="2",
        ),
    )
    second = create_supersession(
        supersession_id="S-AC",
        predecessor=predecessor,
        successor=create_source(
            source_id="C",
            source_version="3",
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "ambiguous successors for "
            "predecessor source"
        ),
    ):
        KnowledgeSourceSupersessionGraph(
            supersessions=(
                first,
                second,
            ),
        )


def test_graph_rejects_two_source_cycle() -> None:
    source_a = create_source(
        source_id="A",
        source_version="1",
    )
    source_b = create_source(
        source_id="B",
        source_version="2",
    )

    with pytest.raises(
        ValueError,
        match="supersession graph must be acyclic",
    ):
        KnowledgeSourceSupersessionGraph(
            supersessions=(
                create_supersession(
                    supersession_id="S-AB",
                    predecessor=source_a,
                    successor=source_b,
                ),
                create_supersession(
                    supersession_id="S-BA",
                    predecessor=source_b,
                    successor=source_a,
                ),
            ),
        )


def test_graph_rejects_three_source_cycle() -> None:
    source_a = create_source(
        source_id="A",
        source_version="1",
    )
    source_b = create_source(
        source_id="B",
        source_version="2",
    )
    source_c = create_source(
        source_id="C",
        source_version="3",
    )

    with pytest.raises(
        ValueError,
        match="supersession graph must be acyclic",
    ):
        KnowledgeSourceSupersessionGraph(
            supersessions=(
                create_supersession(
                    supersession_id="S-AB",
                    predecessor=source_a,
                    successor=source_b,
                ),
                create_supersession(
                    supersession_id="S-BC",
                    predecessor=source_b,
                    successor=source_c,
                ),
                create_supersession(
                    supersession_id="S-CA",
                    predecessor=source_c,
                    successor=source_a,
                ),
            ),
        )


def test_graph_accepts_linear_historical_lineage() -> None:
    source_a = create_source(
        source_id="A",
        source_version="legacy",
    )
    source_b = create_source(
        source_id="B",
        source_version="current",
    )
    source_c = create_source(
        source_id="C",
        source_version="future",
    )

    graph = KnowledgeSourceSupersessionGraph(
        supersessions=(
            create_supersession(
                supersession_id="S-AB",
                predecessor=source_a,
                successor=source_b,
            ),
            create_supersession(
                supersession_id="S-BC",
                predecessor=source_b,
                successor=source_c,
            ),
        ),
    )

    assert len(graph.supersessions) == 2
    assert (
        graph.supersessions[0].predecessor_source_status
        is source_a
    )
    assert (
        graph.supersessions[1].successor_source_status
        is source_c
    )


def test_graph_preserves_predecessor_history() -> None:
    predecessor = create_source(
        source_id="ARCHIVED-SOURCE",
        source_version="legacy",
    )
    supersession = create_supersession(
        predecessor=predecessor,
    )

    graph = KnowledgeSourceSupersessionGraph(
        supersessions=(
            supersession,
        ),
    )

    assert (
        graph.supersessions[0].predecessor_source_status
        is predecessor
    )


def test_supersession_does_not_claim_retrieval_or_authority() -> None:
    graph = KnowledgeSourceSupersessionGraph(
        supersessions=(
            create_supersession(),
        ),
    )

    for attribute in (
        "retrieval_eligible",
        "active_successor",
        "authority_verified",
        "legally_binding",
        "delete_predecessor",
        "commercial_outcome",
    ):
        assert not hasattr(
            graph,
            attribute,
        )
