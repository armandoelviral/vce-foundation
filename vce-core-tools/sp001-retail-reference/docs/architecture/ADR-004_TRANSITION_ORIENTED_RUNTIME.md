# ADR-004 — Transition-Oriented Runtime

Status: Experimental

## Context

The Scientific Product Runtime initially constructed domain objects directly.

RuntimeResult introduced a stable result contract, but lifecycle behavior remained embedded inside Runtime methods.

## Decision

The Runtime shall progressively delegate lifecycle execution to explicit Transition objects.

Each Transition owns one lifecycle movement.

The Runtime coordinates.

Transitions execute.

Domain models represent state.

## Initial Validation

ObjectiveToCaseTransition is the first reference implementation.

## Expected Benefits

- isolated testing;
- transition-level versioning;
- future policy composition;
- invariant evaluation;
- deterministic replay;
- thinner Runtime;
- explicit lifecycle semantics.

## Constraints

Only one Transition shall be migrated before evaluating the pattern.

The remaining Runtime methods shall remain unchanged during this experiment.

## Promotion Condition

ADR-004 may advance beyond Experimental only if the first Transition:

- preserves all existing behavior;
- keeps the complete test suite green;
- reduces responsibility inside the Runtime;
- does not introduce disproportionate complexity.
