# Architectural Decisions

Architectural Decisions define the structural organization of the VCE Research Program.

Unlike Scientific Hypotheses, they govern the architecture of the program itself rather than explain external phenomena.

They remain reviewable and may evolve as the program matures.

---

# AD-001

## Title

Scientific Object-Centered Architecture

## Status

Provisional

---

## Context

The VCE Research Program progressively evolved from a document-centered architecture toward an object-centered architecture.

Scientific knowledge proved to evolve through entities possessing identity, provenance, relationships, lifecycle and epistemic state rather than through isolated documents.

---

## Decision

The Scientific Object is adopted as the fundamental architectural entity of the VCE Research Program.

Within this architecture:

- Scientific Objects constitute the primary units of epistemic evolution.
- The Corpus governs their lifecycle.
- The Registry indexes their epistemic state.
- The Laboratory transforms them through research.
- Scientific Instruments generate them through observation.
- The Runtime provides verifiable execution whenever computational processes participate.

---

## Responsibilities

| Component | Responsibility |
|------------|----------------|
| Scientific Object | Unit of epistemic evolution |
| Corpus | Lifecycle governance |
| Registry | State indexing |
| Laboratory | Scientific transformation |
| Scientific Instruments | Observation generation |
| Runtime | Verifiable execution |

---

## Consequences

Documents are no longer considered first-class entities.

Documents become representations of Scientific Objects.

Scientific knowledge evolves through Scientific Object state transitions.

---

## Scope

This Architectural Decision governs the internal architecture of the VCE Research Program.

It does not claim universality beyond the current research program.

Future Research Cycles may revise this decision if warranted by evidence.

---

## Related Components

- Object Model
- Corpus
- Registry
- Laboratory
- Runtime
