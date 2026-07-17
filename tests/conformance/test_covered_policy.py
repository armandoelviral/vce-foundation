from has.conformance.model.conformance_input import (
    ConformanceInput,
)
from has.conformance.model.decision import (
    Decision,
)
from has.conformance.model.evidence import (
    Evidence,
)
from has.conformance.policies.covered_policy import (
    CoveredPolicy,
)


def test_policy_returns_conformant() -> None:
    decision = CoveredPolicy().evaluate(
        ConformanceInput(
            claim="GP-001",
            capability="Replay",
            executable_contract="contract.py",
            coverage_status="Covered",
        ),
        Evidence(
            source="runtime",
            status="Available",
        ),
    )

    assert decision is Decision.CONFORMANT


def test_policy_returns_non_conformant() -> None:
    decision = CoveredPolicy().evaluate(
        ConformanceInput(
            claim="GP-001",
            capability="Replay",
            executable_contract="contract.py",
            coverage_status="Not Covered",
        ),
        Evidence(
            source="runtime",
            status="Available",
        ),
    )

    assert decision is Decision.NON_CONFORMANT
