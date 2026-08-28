from dataclasses import dataclass
from enum import StrEnum


class KnowledgeDocumentType(StrEnum):
    """Closed knowledge-source document classifications."""

    VISUAL_MANUAL = "VISUAL_MANUAL"
    PLANOGRAM = "PLANOGRAM"
    LOOKBOOK = "LOOKBOOK"
    BUSINESS_RULE = "BUSINESS_RULE"
    SAFETY_GUIDELINE = "SAFETY_GUIDELINE"


class KnowledgeScopeMode(StrEnum):
    """Explicit interpretation of a scoped identity collection."""

    ALL = "ALL"
    EXPLICIT = "EXPLICIT"


@dataclass(frozen=True, slots=True)
class KnowledgeScopeSelection:
    """Immutable all-or-explicit selection without empty-list ambiguity."""

    mode: KnowledgeScopeMode
    ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(
            self.mode,
            KnowledgeScopeMode,
        ):
            raise TypeError(
                "mode must be a KnowledgeScopeMode"
            )

        if not isinstance(
            self.ids,
            tuple,
        ):
            raise TypeError(
                "ids must be an immutable tuple"
            )

        seen_ids: set[str] = set()

        for scoped_id in self.ids:
            if (
                not isinstance(
                    scoped_id,
                    str,
                )
                or not scoped_id.strip()
            ):
                raise ValueError(
                    "scoped id must not be empty"
                )

            if scoped_id in seen_ids:
                raise ValueError(
                    f"duplicate scoped id: {scoped_id}"
                )

            seen_ids.add(
                scoped_id,
            )

        if (
            self.mode is KnowledgeScopeMode.ALL
            and self.ids
        ):
            raise ValueError(
                "ALL scope must not declare explicit ids"
            )

        if (
            self.mode is KnowledgeScopeMode.EXPLICIT
            and not self.ids
        ):
            raise ValueError(
                "EXPLICIT scope requires at least one id"
            )


@dataclass(frozen=True, slots=True)
class KnowledgeSourceScope:
    """Immutable tenant, geography, channel and retail applicability scope."""

    organization_id: str
    customer_id: str
    jurisdiction: str
    commercial_channel_id: str
    document_type: KnowledgeDocumentType
    point_of_sale_scope: KnowledgeScopeSelection
    department_scope: KnowledgeScopeSelection
    campaign_id: str | None = None

    def __post_init__(self) -> None:
        identity_fields = {
            "organization_id": self.organization_id,
            "customer_id": self.customer_id,
            "jurisdiction": self.jurisdiction,
            "commercial_channel_id": (
                self.commercial_channel_id
            ),
        }

        for field, identity in identity_fields.items():
            if (
                not isinstance(
                    identity,
                    str,
                )
                or not identity.strip()
            ):
                raise ValueError(
                    f"{field} must not be empty"
                )

        if not isinstance(
            self.document_type,
            KnowledgeDocumentType,
        ):
            raise TypeError(
                "document_type must be a "
                "KnowledgeDocumentType"
            )

        scope_fields = {
            "point_of_sale_scope": (
                self.point_of_sale_scope
            ),
            "department_scope": self.department_scope,
        }

        for field, selection in scope_fields.items():
            if not isinstance(
                selection,
                KnowledgeScopeSelection,
            ):
                raise TypeError(
                    f"{field} must be a "
                    "KnowledgeScopeSelection"
                )

        if (
            self.campaign_id is not None
            and (
                not isinstance(
                    self.campaign_id,
                    str,
                )
                or not self.campaign_id.strip()
            )
        ):
            raise ValueError(
                "campaign_id must not be empty when declared"
            )
