from dataclasses import dataclass
from decimal import Decimal


def _text(value, name):
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")


def _optional_text(value, name):
    if value is not None:
        _text(value, name)


def _optional_count(value, name):
    if value is not None:
        if type(value) is not int:
            raise TypeError(f"{name} must be an integer or None")
        if value < 0:
            raise ValueError(f"{name} must be nonnegative")


def _ids(values, name, *, optional=False):
    if optional and values is None:
        return
    if type(values) is not tuple:
        raise TypeError(f"{name} must be a tuple")
    for value in values:
        _text(value, name)
    if len(set(values)) != len(values):
        raise ValueError(f"{name} must contain unique identities")


@dataclass(frozen=True, slots=True)
class RetailInspectionSamplePlan:
    """Proposed sample; counts and method are not observations."""
    universe_positions: int | None
    universe_garments: int | None
    planned_positions: tuple[str, ...] | None
    planned_garments: int | None
    selection_method: str | None
    required_coverage: str | None

    def __post_init__(self):
        _optional_count(self.universe_positions, "universe_positions")
        _optional_count(self.universe_garments, "universe_garments")
        _optional_count(self.planned_garments, "planned_garments")
        _ids(self.planned_positions, "planned_positions", optional=True)
        _optional_text(self.selection_method, "selection_method")
        _optional_text(self.required_coverage, "required_coverage")
        if (
            self.universe_positions is not None
            and self.planned_positions is not None
            and len(self.planned_positions) > self.universe_positions
        ):
            raise ValueError("planned positions exceed declared universe")
        if (
            self.universe_garments is not None
            and self.planned_garments is not None
            and self.planned_garments > self.universe_garments
        ):
            raise ValueError("planned garments exceed declared universe")


@dataclass(frozen=True, slots=True)
class RetailInspectionRulePreparation:
    """Proposed rule metadata, not an applicability or criticality decision."""
    rule_id: str
    proposed_requirement: str
    proposed_applicability: str | None
    proposed_criticality: str | None
    applicability_authorization_reference: str | None
    criticality_matrix_reference: str | None

    def __post_init__(self):
        _text(self.rule_id, "rule_id")
        _text(self.proposed_requirement, "proposed_requirement")
        for name in (
            "proposed_applicability", "proposed_criticality",
            "applicability_authorization_reference",
            "criticality_matrix_reference",
        ):
            _optional_text(getattr(self, name), name)


@dataclass(frozen=True, slots=True)
class RetailInspectionCapacityLimitProposal:
    """One declared limit; does not establish its source or approval."""
    value: Decimal
    unit: str
    source_reference: str | None
    measurement_method: str | None
    instrument_reference: str | None

    def __post_init__(self):
        if type(self.value) is not Decimal:
            raise TypeError("value must be a Decimal")
        if not self.value.is_finite() or self.value <= 0:
            raise ValueError("value must be finite and positive")
        _text(self.unit, "unit")
        for name in (
            "source_reference", "measurement_method", "instrument_reference",
        ):
            _optional_text(getattr(self, name), name)


@dataclass(frozen=True, slots=True)
class RetailInspectionPreparation:
    """Preparation declarations; construction grants no authority.

    No evaluations, measurements, coverage, approval or closure are produced.
    An empty capacity tuple means no limits have been recorded, not no limits.
    """
    preparation_id: str
    revision: int
    case_id: str
    declared_store: str
    declared_operator: str
    proposed_protocol_id: str
    proposed_protocol_version: str | None
    proposed_fixture_id: str | None
    sample_plan: RetailInspectionSamplePlan
    rules: tuple[RetailInspectionRulePreparation, ...]
    aggregation_proposal: str
    dispute_resolver_reference: str | None
    capacity_limits: tuple[RetailInspectionCapacityLimitProposal, ...]
    closure_authority_reference: str | None
    closure_blockers: tuple[str, ...]
    candidate_evidence_ids: tuple[str, ...]

    def __post_init__(self):
        for name in (
            "preparation_id", "case_id", "declared_store",
            "declared_operator", "proposed_protocol_id", "aggregation_proposal",
        ):
            _text(getattr(self, name), name)
        for name in (
            "proposed_protocol_version", "proposed_fixture_id",
            "dispute_resolver_reference", "closure_authority_reference",
        ):
            _optional_text(getattr(self, name), name)
        if type(self.revision) is not int:
            raise TypeError("revision must be an integer")
        if self.revision < 1:
            raise ValueError("revision must be positive")
        if type(self.sample_plan) is not RetailInspectionSamplePlan:
            raise TypeError("sample_plan must be a RetailInspectionSamplePlan")
        if type(self.rules) is not tuple or not self.rules:
            raise ValueError("rules must be a nonempty tuple")
        if any(type(rule) is not RetailInspectionRulePreparation
               for rule in self.rules):
            raise TypeError("invalid rule preparation")
        _ids(tuple(rule.rule_id for rule in self.rules), "rule identities")
        if type(self.capacity_limits) is not tuple:
            raise TypeError("capacity_limits must be a tuple")
        if any(type(limit) is not RetailInspectionCapacityLimitProposal
               for limit in self.capacity_limits):
            raise TypeError("invalid capacity limit proposal")
        _ids(self.closure_blockers, "closure_blockers")
        _ids(self.candidate_evidence_ids, "candidate_evidence_ids")
