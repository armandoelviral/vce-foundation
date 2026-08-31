from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.contracts.knowledge_lexical_query import (
    KNOWLEDGE_LEXICAL_NORMALIZATION_POLICY,
    MAXIMUM_LEXICAL_QUERY_ID_LENGTH,
    MAXIMUM_LEXICAL_QUERY_TERM_COUNT,
    MAXIMUM_LEXICAL_QUERY_TERM_LENGTH,
    MAXIMUM_LEXICAL_QUERY_TEXT_LENGTH,
    KnowledgeLexicalQuery,
)


def create_query(
    *,
    query_id: str = "QUERY-001",
    raw_text: str = "Denim wall presentation",
) -> KnowledgeLexicalQuery:
    return KnowledgeLexicalQuery(
        query_id=query_id,
        raw_text=raw_text,
    )


def test_query_is_immutable() -> None:
    query = create_query()

    with pytest.raises(
        FrozenInstanceError,
    ):
        query.normalized_text = "changed"


def test_query_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            KnowledgeLexicalQuery
        )
    ) == (
        "query_id",
        "raw_text",
        "normalized_text",
        "terms",
        "normalization_policy",
    )


def test_query_preserves_identity_and_original_text() -> None:
    query = create_query(
        query_id="QUERY-VM-001",
        raw_text="  Denim   Wall  ",
    )

    assert query.query_id == "QUERY-VM-001"
    assert query.raw_text == "  Denim   Wall  "


def test_query_declares_normalization_policy() -> None:
    query = create_query()

    assert query.normalization_policy == (
        KNOWLEDGE_LEXICAL_NORMALIZATION_POLICY
    )
    assert query.normalization_policy == (
        "NFKC_CASEFOLD_WHITESPACE_V1"
    )


def test_query_applies_nfkc_normalization() -> None:
    query = create_query(
        raw_text="ＤＥＮＩＭ",
    )

    assert query.normalized_text == "denim"
    assert query.terms == (
        "denim",
    )


def test_query_applies_unicode_casefold() -> None:
    query = create_query(
        raw_text="STRASSE Straße",
    )

    assert query.normalized_text == "strasse strasse"
    assert query.terms == (
        "strasse",
        "strasse",
    )


def test_query_collapses_unicode_whitespace() -> None:
    query = create_query(
        raw_text="\tdenim\n\u2003wall\r presentation  ",
    )

    assert query.normalized_text == (
        "denim wall presentation"
    )
    assert query.terms == (
        "denim",
        "wall",
        "presentation",
    )


def test_query_preserves_term_order_and_duplicates() -> None:
    query = create_query(
        raw_text="wall denim wall",
    )

    assert query.terms == (
        "wall",
        "denim",
        "wall",
    )


def test_query_preserves_punctuation_without_interpretation() -> None:
    query = create_query(
        raw_text="boys' denim, wall-display",
    )

    assert query.terms == (
        "boys'",
        "denim,",
        "wall-display",
    )


def test_query_preserves_accents() -> None:
    query = create_query(
        raw_text="NIÑEZ CAFÉ",
    )

    assert query.normalized_text == "niñez café"
    assert query.terms == (
        "niñez",
        "café",
    )


def test_equivalent_inputs_produce_equal_normalized_values() -> None:
    first = create_query(
        raw_text="  Ｄｅｎｉｍ\tWALL ",
    )
    second = create_query(
        raw_text="denim wall",
    )

    assert first.normalized_text == second.normalized_text
    assert first.terms == second.terms


def test_normalization_is_deterministic() -> None:
    first = create_query(
        raw_text="Straße  NIÑEZ",
    )
    second = create_query(
        raw_text="Straße  NIÑEZ",
    )

    assert first == second


def test_query_rejects_untyped_query_id() -> None:
    with pytest.raises(
        TypeError,
        match="query_id must be a string",
    ):
        create_query(
            query_id=1,
        )


@pytest.mark.parametrize(
    "query_id",
    (
        "",
        " ",
        "\n\t",
    ),
)
def test_query_rejects_empty_query_id(
    query_id: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="query_id must not be empty",
    ):
        create_query(
            query_id=query_id,
        )


def test_query_rejects_overlong_query_id() -> None:
    with pytest.raises(
        ValueError,
        match="at most 128 characters",
    ):
        create_query(
            query_id=(
                "Q"
                * (
                    MAXIMUM_LEXICAL_QUERY_ID_LENGTH
                    + 1
                )
            ),
        )


def test_query_rejects_untyped_raw_text() -> None:
    with pytest.raises(
        TypeError,
        match="raw_text must be a string",
    ):
        create_query(
            raw_text=b"denim",
        )


@pytest.mark.parametrize(
    "raw_text",
    (
        "",
        " ",
        "\n\t",
        "\u2003",
    ),
)
def test_query_rejects_text_without_lexical_content(
    raw_text: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="must contain lexical content",
    ):
        create_query(
            raw_text=raw_text,
        )


def test_query_accepts_maximum_raw_text_length() -> None:
    raw_text = (
        (
            "a" * 127
            + " "
        )
        * 7
        + "a" * 127
        + " "
    )

    assert len(
        raw_text
    ) == MAXIMUM_LEXICAL_QUERY_TEXT_LENGTH

    query = create_query(
        raw_text=raw_text,
    )

    assert len(
        query.terms
    ) == 8


def test_query_rejects_overlong_raw_text() -> None:
    with pytest.raises(
        ValueError,
        match="raw_text must contain at most 1024",
    ):
        create_query(
            raw_text=(
                "a"
                * (
                    MAXIMUM_LEXICAL_QUERY_TEXT_LENGTH
                    + 1
                )
            ),
        )


def test_query_rejects_normalization_expansion_over_limit() -> None:
    with pytest.raises(
        ValueError,
        match="normalized_text must contain at most 1024",
    ):
        create_query(
            raw_text=(
                "\ufb03"
                * MAXIMUM_LEXICAL_QUERY_TEXT_LENGTH
            ),
        )


def test_query_accepts_maximum_term_count() -> None:
    query = create_query(
        raw_text=" ".join(
            "a"
            for _ in range(
                MAXIMUM_LEXICAL_QUERY_TERM_COUNT
            )
        ),
    )

    assert len(
        query.terms
    ) == MAXIMUM_LEXICAL_QUERY_TERM_COUNT


def test_query_rejects_excessive_term_count() -> None:
    with pytest.raises(
        ValueError,
        match="terms must contain at most 64",
    ):
        create_query(
            raw_text=" ".join(
                "a"
                for _ in range(
                    MAXIMUM_LEXICAL_QUERY_TERM_COUNT
                    + 1
                )
            ),
        )


def test_query_accepts_maximum_term_length() -> None:
    query = create_query(
        raw_text=(
            "a"
            * MAXIMUM_LEXICAL_QUERY_TERM_LENGTH
        ),
    )

    assert len(
        query.terms[0]
    ) == MAXIMUM_LEXICAL_QUERY_TERM_LENGTH


def test_query_rejects_excessive_term_length() -> None:
    with pytest.raises(
        ValueError,
        match="each lexical term must contain at most 128",
    ):
        create_query(
            raw_text=(
                "a"
                * (
                    MAXIMUM_LEXICAL_QUERY_TERM_LENGTH
                    + 1
                )
            ),
        )


def test_query_rejects_control_characters() -> None:
    with pytest.raises(
        ValueError,
        match="must not contain control characters",
    ):
        create_query(
            raw_text="denim\x01wall",
        )


def test_query_does_not_claim_matching_or_relevance() -> None:
    names = {
        field.name
        for field in fields(
            KnowledgeLexicalQuery
        )
    }

    assert "matches" not in names
    assert "score" not in names
    assert "ranking" not in names
    assert "relevance" not in names
    assert "intent" not in names
    assert "embedding" not in names
