from dataclasses import dataclass
from typing import Protocol, runtime_checkable


def _validate_text(name: str, value: object) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True, slots=True)
class RetailRuleEvaluationReportIdentity:
    """Opaque identity for one report emission within a store namespace."""

    report_id: str

    def __post_init__(self) -> None:
        _validate_text("report_id", self.report_id)


@dataclass(frozen=True, slots=True)
class StoredRetailRuleEvaluationReport:
    """Exact document bound to an emission identity; no authenticity claims."""

    identity: RetailRuleEvaluationReportIdentity
    document: str

    def __post_init__(self) -> None:
        if not isinstance(
            self.identity, RetailRuleEvaluationReportIdentity
        ):
            raise TypeError(
                "identity must be a RetailRuleEvaluationReportIdentity"
            )
        _validate_text("document", self.document)


class RetailRuleEvaluationReportConflict(RuntimeError):
    """The emission identity is already bound to a different document."""


@runtime_checkable
class RetailRuleEvaluationReportStore(Protocol):
    """Append-only port for exact report documents.

    The adapter must enforce identity uniqueness atomically.
    No update or deletion operation is offered by this port.
    Infrastructure failures must propagate, never become absence.
    Document schema validation belongs to the caller's codec boundary.
    """

    def put(
        self, *, report: StoredRetailRuleEvaluationReport
    ) -> StoredRetailRuleEvaluationReport:
        """Persist and confirm, or return the identical existing record.

        Same identity with different document text must raise
        RetailRuleEvaluationReportConflict without modifying stored data.
        A return value confirms persistence; an exception may leave the
        outcome unknown, so callers may recover by the same identity.
        """
        ...

    def get(
        self, *, identity: RetailRuleEvaluationReportIdentity
    ) -> StoredRetailRuleEvaluationReport | None:
        """Return the exact stored record, or None only when absent."""
        ...
