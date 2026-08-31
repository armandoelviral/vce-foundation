import pytest

import sp001.contracts.knowledge_lexical_query as query_module
from sp001.contracts.knowledge_lexical_query import (
    KnowledgeLexicalQuery,
)
from sp001.services.knowledge_lexical_text_normalization import (
    KNOWLEDGE_LEXICAL_NORMALIZATION_POLICY,
    normalize_knowledge_lexical_text,
)


def normalize(
    text: str,
) -> str:
    return normalize_knowledge_lexical_text(
        text=text,
    )


def test_normalization_policy_is_explicit() -> None:
    assert KNOWLEDGE_LEXICAL_NORMALIZATION_POLICY == (
        "NFKC_CASEFOLD_WHITESPACE_V1"
    )


@pytest.mark.parametrize(
    "text",
    (
        None,
        b"denim",
        1,
        object(),
    ),
)
def test_normalizer_rejects_untyped_text(
    text: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="text must be a string",
    ):
        normalize_knowledge_lexical_text(
            text=text,
        )


@pytest.mark.parametrize(
    "text",
    (
        "",
        " ",
        "\n\t",
        "\u2003",
    ),
)
def test_normalizer_allows_empty_normalized_result(
    text: str,
) -> None:
    assert normalize(
        text
    ) == ""


def test_normalizer_applies_nfkc() -> None:
    assert normalize(
        "ＤＥＮＩＭ"
    ) == "denim"


def test_normalizer_applies_casefold() -> None:
    assert normalize(
        "STRASSE Straße"
    ) == "strasse strasse"


def test_normalizer_collapses_unicode_whitespace() -> None:
    assert normalize(
        "\tdenim\n\u2003wall\r presentation  "
    ) == "denim wall presentation"


def test_normalizer_preserves_accents() -> None:
    assert normalize(
        "NIÑEZ CAFÉ"
    ) == "niñez café"


def test_normalizer_preserves_punctuation() -> None:
    assert normalize(
        "boys' denim, wall-display"
    ) == "boys' denim, wall-display"


def test_normalizer_preserves_duplicate_lexical_values() -> None:
    assert normalize(
        "wall  denim wall"
    ) == "wall denim wall"


def test_normalizer_rejects_remaining_control_characters() -> None:
    with pytest.raises(
        ValueError,
        match="must not contain control characters",
    ):
        normalize(
            "denim\x01wall"
        )


def test_normalizer_is_deterministic() -> None:
    first = normalize(
        "  Straße ＤＥＮＩＭ  "
    )
    second = normalize(
        "  Straße ＤＥＮＩＭ  "
    )

    assert first == second


def test_normalizer_is_idempotent() -> None:
    first = normalize(
        "  Straße ＤＥＮＩＭ  "
    )
    second = normalize(
        first
    )

    assert second == first


def test_query_reuses_shared_normalization_policy() -> None:
    query = KnowledgeLexicalQuery(
        query_id="QUERY-001",
        raw_text=" ＤＥＮＩＭ  Straße ",
    )

    assert query.normalized_text == (
        normalize(
            query.raw_text
        )
    )
    assert query.normalization_policy == (
        KNOWLEDGE_LEXICAL_NORMALIZATION_POLICY
    )


def test_query_delegates_to_shared_normalizer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = []

    def normalize_stub(
        *,
        text: str,
    ) -> str:
        calls.append(
            text
        )
        return "delegated lexical text"

    monkeypatch.setattr(
        query_module,
        "normalize_knowledge_lexical_text",
        normalize_stub,
    )

    query = KnowledgeLexicalQuery(
        query_id="QUERY-001",
        raw_text="Original Text",
    )

    assert calls == [
        "Original Text",
    ]
    assert query.normalized_text == "delegated lexical text"
    assert query.terms == (
        "delegated",
        "lexical",
        "text",
    )


def test_normalizer_introduces_no_matching_result() -> None:
    result = normalize(
        "denim wall"
    )

    assert isinstance(
        result,
        str,
    )
    assert result == "denim wall"
