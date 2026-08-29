from dataclasses import FrozenInstanceError, replace

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
from sp001.services.knowledge_source_integrity import (
    digest_knowledge_source_content,
)


SOURCE_BYTES = b"original source bytes"
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
    artifact_id: str = "ARTIFACT-001",
) -> KnowledgeDerivedArtifactIdentity:
    return KnowledgeDerivedArtifactIdentity(
        artifact_id=artifact_id,
        artifact_version="v1",
        source_identity=source_identity(),
        extraction_identity=extraction_identity(),
        artifact_content_digest=digest(ARTIFACT_BYTES),
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


def test_extraction_preserves_tool_version_and_configuration() -> None:
    extraction = extraction_identity()

    assert extraction.extractor_id == "TEXT-EXTRACTOR"
    assert extraction.extractor_version == "1.0.0"
    assert extraction.configuration_digest == digest(
        CONFIG_BYTES
    )


@pytest.mark.parametrize(
    "field",
    (
        "extraction_id",
        "extractor_id",
        "extractor_version",
    ),
)
def test_extraction_rejects_empty_identity(
    field: str,
) -> None:
    values = {
        "extraction_id": "EXTRACTION-001",
        "extractor_id": "TEXT-EXTRACTOR",
        "extractor_version": "1.0.0",
        "configuration_digest": digest(CONFIG_BYTES),
    }
    values[field] = " "

    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        KnowledgeExtractionIdentity(**values)


def test_extraction_rejects_untyped_configuration_digest() -> None:
    with pytest.raises(
        TypeError,
        match="configuration_digest",
    ):
        KnowledgeExtractionIdentity(
            extraction_id="EXTRACTION-001",
            extractor_id="TEXT-EXTRACTOR",
            extractor_version="1.0.0",
            configuration_digest="digest",
        )


def test_artifact_preserves_source_and_extraction_lineage() -> None:
    artifact = artifact_identity()

    assert artifact.source_identity.source_id == "SOURCE-001"
    assert artifact.extraction_identity.extraction_id == (
        "EXTRACTION-001"
    )
    assert artifact.artifact_content_digest == digest(
        ARTIFACT_BYTES
    )


@pytest.mark.parametrize(
    "field",
    (
        "artifact_id",
        "artifact_version",
    ),
)
def test_artifact_rejects_empty_identity(
    field: str,
) -> None:
    artifact = artifact_identity()
    values = {
        "artifact_id": artifact.artifact_id,
        "artifact_version": artifact.artifact_version,
        "source_identity": artifact.source_identity,
        "extraction_identity": artifact.extraction_identity,
        "artifact_content_digest": (
            artifact.artifact_content_digest
        ),
    }
    values[field] = ""

    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        KnowledgeDerivedArtifactIdentity(**values)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        (
            "source_identity",
            "source",
            "source_identity must be a",
        ),
        (
            "extraction_identity",
            "extraction",
            "extraction_identity must be a",
        ),
        (
            "artifact_content_digest",
            "digest",
            "artifact_content_digest must be a",
        ),
    ),
)
def test_artifact_rejects_untyped_lineage(
    field: str,
    value: object,
    message: str,
) -> None:
    artifact = artifact_identity()
    values = {
        "artifact_id": artifact.artifact_id,
        "artifact_version": artifact.artifact_version,
        "source_identity": artifact.source_identity,
        "extraction_identity": artifact.extraction_identity,
        "artifact_content_digest": (
            artifact.artifact_content_digest
        ),
    }
    values[field] = value

    with pytest.raises(TypeError, match=message):
        KnowledgeDerivedArtifactIdentity(**values)


def test_fragment_preserves_half_open_byte_range() -> None:
    artifact = artifact_identity()
    item = fragment(
        fragment_id="FRAGMENT-001",
        sequence_number=0,
        byte_start=0,
        byte_end=14,
        content=b"first fragment",
        artifact=artifact,
    )

    assert item.artifact_identity is artifact
    assert (item.byte_start, item.byte_end) == (0, 14)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        ("sequence_number", -1, "must not be negative"),
        ("byte_start", -1, "must not be negative"),
        ("byte_end", 0, "must be greater than"),
    ),
)
def test_fragment_rejects_invalid_boundaries(
    field: str,
    value: int,
    message: str,
) -> None:
    values = {
        "fragment_id": "FRAGMENT-001",
        "artifact_identity": artifact_identity(),
        "sequence_number": 0,
        "byte_start": 0,
        "byte_end": 14,
        "fragment_content_digest": digest(
            b"first fragment"
        ),
    }
    values[field] = value

    with pytest.raises(ValueError, match=message):
        KnowledgeFragmentIdentity(**values)


@pytest.mark.parametrize(
    "field",
    (
        "sequence_number",
        "byte_start",
        "byte_end",
    ),
)
def test_fragment_rejects_boolean_integer(
    field: str,
) -> None:
    values = {
        "fragment_id": "FRAGMENT-001",
        "artifact_identity": artifact_identity(),
        "sequence_number": 0,
        "byte_start": 0,
        "byte_end": 14,
        "fragment_content_digest": digest(
            b"first fragment"
        ),
    }
    values[field] = True

    with pytest.raises(
        TypeError,
        match=f"{field} must be an integer",
    ):
        KnowledgeFragmentIdentity(**values)


def test_empty_fragment_set_is_explicitly_valid() -> None:
    artifact = artifact_identity()
    fragment_set = KnowledgeFragmentSet(
        artifact_identity=artifact,
        fragments=(),
    )

    assert fragment_set.fragments == ()


def test_fragment_set_preserves_declared_order() -> None:
    artifact = artifact_identity()
    first = fragment(
        fragment_id="FRAGMENT-001",
        sequence_number=0,
        byte_start=0,
        byte_end=14,
        content=b"first fragment",
        artifact=artifact,
    )
    second = fragment(
        fragment_id="FRAGMENT-002",
        sequence_number=1,
        byte_start=14,
        byte_end=29,
        content=b"second fragment",
        artifact=artifact,
    )

    fragment_set = KnowledgeFragmentSet(
        artifact_identity=artifact,
        fragments=(first, second),
    )

    assert fragment_set.fragments == (first, second)


def test_fragment_set_rejects_cross_artifact_fragment() -> None:
    artifact = artifact_identity()
    other = artifact_identity(
        artifact_id="ARTIFACT-OTHER",
    )
    item = fragment(
        fragment_id="FRAGMENT-001",
        sequence_number=0,
        byte_start=0,
        byte_end=14,
        content=b"first fragment",
        artifact=other,
    )

    with pytest.raises(
        ValueError,
        match="fragment must reference set artifact",
    ):
        KnowledgeFragmentSet(
            artifact_identity=artifact,
            fragments=(item,),
        )


def test_fragment_set_rejects_duplicate_fragment_identity() -> None:
    artifact = artifact_identity()
    item = fragment(
        fragment_id="FRAGMENT-001",
        sequence_number=0,
        byte_start=0,
        byte_end=14,
        content=b"first fragment",
        artifact=artifact,
    )

    with pytest.raises(
        ValueError,
        match="duplicate fragment_id",
    ):
        KnowledgeFragmentSet(
            artifact_identity=artifact,
            fragments=(item, item),
        )


def test_fragment_set_rejects_duplicate_sequence_number() -> None:
    artifact = artifact_identity()
    first = fragment(
        fragment_id="FRAGMENT-001",
        sequence_number=0,
        byte_start=0,
        byte_end=14,
        content=b"first fragment",
        artifact=artifact,
    )
    second = fragment(
        fragment_id="FRAGMENT-002",
        sequence_number=0,
        byte_start=14,
        byte_end=29,
        content=b"second fragment",
        artifact=artifact,
    )

    with pytest.raises(
        ValueError,
        match="duplicate fragment sequence_number",
    ):
        KnowledgeFragmentSet(
            artifact_identity=artifact,
            fragments=(first, second),
        )


def test_fragment_set_rejects_overlapping_ranges() -> None:
    artifact = artifact_identity()
    first = fragment(
        fragment_id="FRAGMENT-001",
        sequence_number=0,
        byte_start=0,
        byte_end=14,
        content=b"first fragment",
        artifact=artifact,
    )
    second = fragment(
        fragment_id="FRAGMENT-002",
        sequence_number=1,
        byte_start=10,
        byte_end=25,
        content=b"overlap bytes",
        artifact=artifact,
    )

    with pytest.raises(
        ValueError,
        match="fragments must not overlap",
    ):
        KnowledgeFragmentSet(
            artifact_identity=artifact,
            fragments=(first, second),
        )


def test_identities_are_immutable() -> None:
    extraction = extraction_identity()
    artifact = artifact_identity()

    with pytest.raises(FrozenInstanceError):
        extraction.extractor_version = "2.0.0"

    with pytest.raises(FrozenInstanceError):
        artifact.artifact_version = "v2"


def test_identity_construction_does_not_verify_byte_derivation() -> None:
    artifact = artifact_identity()
    item = fragment(
        fragment_id="FRAGMENT-001",
        sequence_number=0,
        byte_start=0,
        byte_end=14,
        content=b"different bytes",
        artifact=artifact,
    )

    assert item.fragment_content_digest != digest(
        ARTIFACT_BYTES[0:14]
    )

    for attribute in (
        "derivation_verified",
        "extraction_correct",
        "semantic_relevance",
        "embedding",
        "ocr_confidence",
        "authority",
        "truth",
    ):
        assert not hasattr(item, attribute)


def test_identity_construction_does_not_mutate_lineage() -> None:
    source = source_identity()
    source_before = replace(source)

    KnowledgeDerivedArtifactIdentity(
        artifact_id="ARTIFACT-001",
        artifact_version="v1",
        source_identity=source,
        extraction_identity=extraction_identity(),
        artifact_content_digest=digest(ARTIFACT_BYTES),
    )

    assert source == source_before
