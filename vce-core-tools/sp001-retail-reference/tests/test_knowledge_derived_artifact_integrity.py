from dataclasses import replace

import pytest

from sp001.contracts.knowledge_derived_artifact import (
    KnowledgeDerivedArtifactIdentity,
    KnowledgeExtractionIdentity,
    KnowledgeFragmentIdentity,
    KnowledgeFragmentSet,
)
from sp001.contracts.knowledge_source_identity import (
    KnowledgeSourceIdentity,
)
from sp001.services.knowledge_derived_artifact_integrity import (
    verify_knowledge_derived_artifact_content,
    verify_knowledge_fragment_content,
    verify_knowledge_fragment_set_content,
)
from sp001.services.knowledge_source_integrity import (
    digest_knowledge_source_content,
)


SOURCE_BYTES = b"original PDF bytes"
CONFIG_BYTES = b'{"mode":"text"}'
ARTIFACT_BYTES = b"first fragmentsecond fragment"


def digest(content: bytes):
    return digest_knowledge_source_content(
        content=content,
    )


def source_identity() -> KnowledgeSourceIdentity:
    return KnowledgeSourceIdentity(
        source_id="SOURCE-001",
        source_version="v1",
        source_content_digest=digest(SOURCE_BYTES),
    )


def extraction_identity() -> KnowledgeExtractionIdentity:
    return KnowledgeExtractionIdentity(
        extraction_id="EXTRACTION-001",
        extractor_id="TEXT-EXTRACTOR",
        extractor_version="1.0.0",
        configuration_digest=digest(CONFIG_BYTES),
    )


def artifact_identity(
    *,
    content: bytes = ARTIFACT_BYTES,
) -> KnowledgeDerivedArtifactIdentity:
    return KnowledgeDerivedArtifactIdentity(
        artifact_id="ARTIFACT-001",
        artifact_version="v1",
        source_identity=source_identity(),
        extraction_identity=extraction_identity(),
        artifact_content_digest=digest(content),
    )


def fragment(
    *,
    fragment_id: str,
    sequence_number: int,
    byte_start: int,
    byte_end: int,
    content: bytes,
    artifact=None,
) -> KnowledgeFragmentIdentity:
    return KnowledgeFragmentIdentity(
        fragment_id=fragment_id,
        artifact_identity=artifact or artifact_identity(),
        sequence_number=sequence_number,
        byte_start=byte_start,
        byte_end=byte_end,
        fragment_content_digest=digest(content),
    )


def fragment_set() -> KnowledgeFragmentSet:
    artifact = artifact_identity()

    return KnowledgeFragmentSet(
        artifact_identity=artifact,
        fragments=(
            fragment(
                fragment_id="FRAGMENT-001",
                sequence_number=0,
                byte_start=0,
                byte_end=14,
                content=b"first fragment",
                artifact=artifact,
            ),
            fragment(
                fragment_id="FRAGMENT-002",
                sequence_number=1,
                byte_start=14,
                byte_end=29,
                content=b"second fragment",
                artifact=artifact,
            ),
        ),
    )


def test_artifact_verification_accepts_matching_bytes() -> None:
    assert verify_knowledge_derived_artifact_content(
        identity=artifact_identity(),
        content=ARTIFACT_BYTES,
    )


def test_artifact_verification_rejects_modified_bytes() -> None:
    assert not verify_knowledge_derived_artifact_content(
        identity=artifact_identity(),
        content=b"modified artifact bytes",
    )


def test_artifact_verification_preserves_exact_byte_semantics() -> None:
    identity = artifact_identity(
        content="café".encode("utf-8"),
    )

    assert verify_knowledge_derived_artifact_content(
        identity=identity,
        content="café".encode("utf-8"),
    )

    assert not verify_knowledge_derived_artifact_content(
        identity=identity,
        content="cafe".encode("utf-8"),
    )


def test_artifact_verification_rejects_untyped_identity() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeDerivedArtifactIdentity",
    ):
        verify_knowledge_derived_artifact_content(
            identity="artifact",
            content=ARTIFACT_BYTES,
        )


@pytest.mark.parametrize(
    "content",
    (
        bytearray(ARTIFACT_BYTES),
        "artifact",
    ),
)
def test_verification_rejects_mutable_or_nonbyte_content(
    content: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="content must be immutable bytes",
    ):
        verify_knowledge_derived_artifact_content(
            identity=artifact_identity(),
            content=content,
        )


def test_verification_rejects_empty_content() -> None:
    with pytest.raises(
        ValueError,
        match="content must not be empty",
    ):
        verify_knowledge_derived_artifact_content(
            identity=artifact_identity(),
            content=b"",
        )


def test_fragment_verification_accepts_exact_declared_slice() -> None:
    item = fragment_set().fragments[0]

    assert verify_knowledge_fragment_content(
        fragment=item,
        artifact_content=ARTIFACT_BYTES,
    )


def test_fragment_verification_rejects_modified_slice() -> None:
    item = fragment_set().fragments[0]
    modified = b"wrong fragment!" + ARTIFACT_BYTES[14:]

    assert not verify_knowledge_fragment_content(
        fragment=item,
        artifact_content=modified,
    )


def test_fragment_verification_rejects_out_of_bounds_range() -> None:
    artifact = artifact_identity()
    item = fragment(
        fragment_id="FRAGMENT-OUTSIDE",
        sequence_number=0,
        byte_start=20,
        byte_end=40,
        content=b"declared outside bytes",
        artifact=artifact,
    )

    assert not verify_knowledge_fragment_content(
        fragment=item,
        artifact_content=ARTIFACT_BYTES,
    )


def test_fragment_verification_rejects_untyped_fragment() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeFragmentIdentity",
    ):
        verify_knowledge_fragment_content(
            fragment="fragment",
            artifact_content=ARTIFACT_BYTES,
        )


def test_fragment_set_verification_preserves_declared_order() -> None:
    results = verify_knowledge_fragment_set_content(
        fragment_set=fragment_set(),
        artifact_content=ARTIFACT_BYTES,
    )

    assert results == (True, True)


def test_fragment_set_reports_each_result_independently() -> None:
    declared_set = fragment_set()
    modified = ARTIFACT_BYTES[:14] + b"modified bytes!"

    results = verify_knowledge_fragment_set_content(
        fragment_set=declared_set,
        artifact_content=modified,
    )

    assert results == (True, False)


def test_empty_fragment_set_produces_empty_result() -> None:
    artifact = artifact_identity()
    declared_set = KnowledgeFragmentSet(
        artifact_identity=artifact,
        fragments=(),
    )

    assert verify_knowledge_fragment_set_content(
        fragment_set=declared_set,
        artifact_content=ARTIFACT_BYTES,
    ) == ()


def test_fragment_set_verification_rejects_untyped_set() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeFragmentSet",
    ):
        verify_knowledge_fragment_set_content(
            fragment_set="fragment-set",
            artifact_content=ARTIFACT_BYTES,
        )


def test_fragment_verification_does_not_require_full_artifact_match() -> None:
    declared_set = fragment_set()
    first = declared_set.fragments[0]
    modified_tail = ARTIFACT_BYTES[:14] + b"changed tail!!!"

    assert verify_knowledge_fragment_content(
        fragment=first,
        artifact_content=modified_tail,
    )

    assert not verify_knowledge_derived_artifact_content(
        identity=declared_set.artifact_identity,
        content=modified_tail,
    )


def test_verification_does_not_mutate_identities() -> None:
    identity = artifact_identity()
    identity_before = replace(identity)

    verify_knowledge_derived_artifact_content(
        identity=identity,
        content=ARTIFACT_BYTES,
    )

    assert identity == identity_before


def test_byte_correspondence_does_not_claim_extraction_quality() -> None:
    identity = artifact_identity()

    assert verify_knowledge_derived_artifact_content(
        identity=identity,
        content=ARTIFACT_BYTES,
    )

    for attribute in (
        "extraction_correct",
        "ocr_accurate",
        "semantically_equivalent",
        "source_authentic",
        "authority_verified",
        "relevant",
        "truth",
    ):
        assert not hasattr(identity, attribute)
