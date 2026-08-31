import unicodedata


KNOWLEDGE_LEXICAL_NORMALIZATION_POLICY = (
    "NFKC_CASEFOLD_WHITESPACE_V1"
)


def normalize_knowledge_lexical_text(
    *,
    text: str,
) -> str:
    """Normalize lexical text without matching or relevance claims."""

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string"
        )

    normalized = unicodedata.normalize(
        "NFKC",
        unicodedata.normalize(
            "NFKC",
            text,
        ).casefold(),
    )
    normalized = " ".join(
        normalized.split()
    )

    if any(
        unicodedata.category(
            character
        ) == "Cc"
        for character in normalized
    ):
        raise ValueError(
            "normalized text must not contain "
            "control characters"
        )

    return normalized
