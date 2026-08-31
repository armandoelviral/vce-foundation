from dataclasses import dataclass, field
import unicodedata


KNOWLEDGE_LEXICAL_NORMALIZATION_POLICY = (
    "NFKC_CASEFOLD_WHITESPACE_V1"
)
MAXIMUM_LEXICAL_QUERY_ID_LENGTH = 128
MAXIMUM_LEXICAL_QUERY_TEXT_LENGTH = 1024
MAXIMUM_LEXICAL_QUERY_TERM_COUNT = 64
MAXIMUM_LEXICAL_QUERY_TERM_LENGTH = 128


@dataclass(frozen=True, slots=True)
class KnowledgeLexicalQuery:
    """Bounded normalized lexical input without relevance claims."""

    query_id: str
    raw_text: str
    normalized_text: str = field(
        init=False,
    )
    terms: tuple[str, ...] = field(
        init=False,
    )
    normalization_policy: str = field(
        init=False,
        default=KNOWLEDGE_LEXICAL_NORMALIZATION_POLICY,
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.query_id,
            str,
        ):
            raise TypeError(
                "query_id must be a string"
            )
        if not self.query_id.strip():
            raise ValueError(
                "query_id must not be empty"
            )
        if len(
            self.query_id
        ) > MAXIMUM_LEXICAL_QUERY_ID_LENGTH:
            raise ValueError(
                "query_id must contain at most "
                "128 characters"
            )

        if not isinstance(
            self.raw_text,
            str,
        ):
            raise TypeError(
                "raw_text must be a string"
            )
        if len(
            self.raw_text
        ) > MAXIMUM_LEXICAL_QUERY_TEXT_LENGTH:
            raise ValueError(
                "raw_text must contain at most "
                "1024 characters"
            )

        normalized = unicodedata.normalize(
            "NFKC",
            unicodedata.normalize(
                "NFKC",
                self.raw_text,
            ).casefold(),
        )
        normalized = " ".join(
            normalized.split()
        )

        if not normalized:
            raise ValueError(
                "raw_text must contain lexical content"
            )
        if len(
            normalized
        ) > MAXIMUM_LEXICAL_QUERY_TEXT_LENGTH:
            raise ValueError(
                "normalized_text must contain at most "
                "1024 characters"
            )
        if any(
            unicodedata.category(
                character
            ) == "Cc"
            for character in normalized
        ):
            raise ValueError(
                "normalized_text must not contain "
                "control characters"
            )

        terms = tuple(
            normalized.split(" ")
        )

        if len(
            terms
        ) > MAXIMUM_LEXICAL_QUERY_TERM_COUNT:
            raise ValueError(
                "terms must contain at most 64 values"
            )

        for term in terms:
            if len(
                term
            ) > MAXIMUM_LEXICAL_QUERY_TERM_LENGTH:
                raise ValueError(
                    "each lexical term must contain "
                    "at most 128 characters"
                )

        object.__setattr__(
            self,
            "normalized_text",
            normalized,
        )
        object.__setattr__(
            self,
            "terms",
            terms,
        )
