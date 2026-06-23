from dataclasses import dataclass


VALID_INSTITUTIONAL_CAPITAL_DOMAINS = {
    "compliance",
    "governance",
    "reputation",
    "constitutional_behavior",
}


@dataclass(frozen=True)
class InstitutionalCapitalRecord:
    institution_id: str
    evidence_id: str
    source_domain: str
    capital_delta: int
    reason: str

    def __post_init__(self):
        if not self.institution_id:
            raise ValueError("institution_id is required")

        if not self.evidence_id:
            raise ValueError("evidence_id is required")

        if self.source_domain not in VALID_INSTITUTIONAL_CAPITAL_DOMAINS:
            raise ValueError(f"invalid source_domain: {self.source_domain}")

        if self.capital_delta == 0:
            raise ValueError("capital_delta cannot be zero")

        if not self.reason:
            raise ValueError("reason is required")
