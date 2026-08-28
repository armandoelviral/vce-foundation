import hashlib
import hmac

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)


def digest_knowledge_source_content(
    *,
    content: bytes,
) -> KnowledgeContentDigest:
    """Digest exact source bytes without interpreting their meaning."""

    _validate_content(
        content,
    )

    return KnowledgeContentDigest(
        algorithm="SHA-256",
        value=hashlib.sha256(
            content,
        ).hexdigest(),
    )


def verify_knowledge_source_content(
    *,
    identity: KnowledgeSourceIdentity,
    content: bytes,
) -> bool:
    """Verify byte correspondence without asserting source authenticity."""

    if not isinstance(
        identity,
        KnowledgeSourceIdentity,
    ):
        raise TypeError(
            "identity must be a KnowledgeSourceIdentity"
        )

    _validate_content(
        content,
    )

    observed_digest = digest_knowledge_source_content(
        content=content,
    )

    return hmac.compare_digest(
        identity.source_content_digest.value,
        observed_digest.value,
    )


def _validate_content(
    content: object,
) -> None:
    if not isinstance(
        content,
        bytes,
    ):
        raise TypeError(
            "content must be immutable bytes"
        )

    if not content:
        raise ValueError(
            "content must not be empty"
        )
