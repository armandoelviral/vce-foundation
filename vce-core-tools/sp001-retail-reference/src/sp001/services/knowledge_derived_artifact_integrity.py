import hmac

from sp001.contracts.knowledge_derived_artifact import (
    KnowledgeDerivedArtifactIdentity,
    KnowledgeFragmentIdentity,
    KnowledgeFragmentSet,
)
from sp001.services.knowledge_source_integrity import (
    digest_knowledge_source_content,
)


def verify_knowledge_derived_artifact_content(
    *,
    identity: KnowledgeDerivedArtifactIdentity,
    content: bytes,
) -> bool:
    """Verify exact artifact bytes without validating extraction quality."""

    if not isinstance(
        identity,
        KnowledgeDerivedArtifactIdentity,
    ):
        raise TypeError(
            "identity must be a "
            "KnowledgeDerivedArtifactIdentity"
        )

    _validate_content(content)

    observed_digest = digest_knowledge_source_content(
        content=content,
    )

    return hmac.compare_digest(
        identity.artifact_content_digest.value,
        observed_digest.value,
    )


def verify_knowledge_fragment_content(
    *,
    fragment: KnowledgeFragmentIdentity,
    artifact_content: bytes,
) -> bool:
    """Verify one declared half-open range against supplied artifact bytes."""

    if not isinstance(
        fragment,
        KnowledgeFragmentIdentity,
    ):
        raise TypeError(
            "fragment must be a KnowledgeFragmentIdentity"
        )

    _validate_content(artifact_content)

    if fragment.byte_end > len(artifact_content):
        return False

    fragment_content = artifact_content[
        fragment.byte_start:fragment.byte_end
    ]

    if not fragment_content:
        return False

    observed_digest = digest_knowledge_source_content(
        content=fragment_content,
    )

    return hmac.compare_digest(
        fragment.fragment_content_digest.value,
        observed_digest.value,
    )


def verify_knowledge_fragment_set_content(
    *,
    fragment_set: KnowledgeFragmentSet,
    artifact_content: bytes,
) -> tuple[bool, ...]:
    """Verify all fragments independently in declared order."""

    if not isinstance(
        fragment_set,
        KnowledgeFragmentSet,
    ):
        raise TypeError(
            "fragment_set must be a KnowledgeFragmentSet"
        )

    _validate_content(artifact_content)

    return tuple(
        verify_knowledge_fragment_content(
            fragment=fragment,
            artifact_content=artifact_content,
        )
        for fragment in fragment_set.fragments
    )


def _validate_content(content: object) -> None:
    if not isinstance(content, bytes):
        raise TypeError(
            "content must be immutable bytes"
        )

    if not content:
        raise ValueError(
            "content must not be empty"
        )
