from epics.ztc25_formal_verification_certification.formal_invariant import (
    FormalInvariant,
)

from epics.ztc25_formal_verification_certification.invariant_registry import (
    InvariantRegistry,
)


def test_registry_stores_invariant():

    registry = InvariantRegistry()

    invariant = FormalInvariant(
        invariant_id="INV-001",
        description="sequence never decreases",
    )

    registry.add(invariant)

    assert registry.count() == 1


def test_registry_reports_known_invariant():

    registry = InvariantRegistry()

    invariant = FormalInvariant(
        invariant_id="INV-001",
        description="sequence never decreases",
    )

    registry.add(invariant)

    assert registry.exists("INV-001")


def test_registry_returns_invariants():

    registry = InvariantRegistry()

    invariant = FormalInvariant(
        invariant_id="INV-001",
        description="sequence never decreases",
    )

    registry.add(invariant)

    assert registry.all()[0].invariant_id == "INV-001"
