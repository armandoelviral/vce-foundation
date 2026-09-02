import json

from sp001.contracts.knowledge_governed_retrieval_evidence import (
    KnowledgeGovernedRetrievalEvidence,
)
from sp001.services.knowledge_governed_retrieval_lexical_projection import (
    project_knowledge_lexical_ordering,
)
from sp001.services.knowledge_governed_retrieval_manifest_projection import (
    project_knowledge_retrieval_manifest,
)
from sp001.services.knowledge_governed_retrieval_query_context_projection import (
    project_knowledge_lexical_query,
)


def serialize_knowledge_governed_retrieval_evidence(
    *,
    evidence: KnowledgeGovernedRetrievalEvidence,
) -> str:
    """Serialize validated retrieval evidence to canonical JSON text."""

    if not isinstance(
        evidence,
        KnowledgeGovernedRetrievalEvidence,
    ):
        raise TypeError(
            "evidence must be a "
            "KnowledgeGovernedRetrievalEvidence"
        )

    result = evidence.result

    document = {
        "schema_version": evidence.schema_version,
        "counts": {
            "candidate_count": evidence.candidate_count,
            "included_candidate_count": (
                evidence.included_candidate_count
            ),
            "excluded_candidate_count": (
                evidence.excluded_candidate_count
            ),
            "ordered_candidate_count": (
                evidence.ordered_candidate_count
            ),
        },
        "result": {
            "query": project_knowledge_lexical_query(
                query=result.query,
            ),
            "manifest": project_knowledge_retrieval_manifest(
                manifest=result.manifest,
            ),
            "lexical_ordering": (
                project_knowledge_lexical_ordering(
                    ordering=result.lexical_ordering,
                )
            ),
        },
    }

    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
