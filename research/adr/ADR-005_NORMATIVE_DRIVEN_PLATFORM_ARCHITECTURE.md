# ADR-005

Normative-Driven Platform Architecture

Status

Accepted

---

## Context

HAS Foundation consists of multiple
independent platforms.

Although implemented independently,
all platforms converged toward the
same architectural structure.

This ADR documents that structure as
the normative architectural pattern.

---

## Decision

Every HAS platform shall follow the
same layered architecture.

Normative Documents

↓

Executable Contracts

↓

Domain Model

↓

Policies

↓

Evaluator

↓

Pipeline

↓

End-to-End Flow

---

## Rationale

Normative documents define meaning.

Executable contracts verify meaning.

Domain models represent meaning.

Policies implement normative rules.

Evaluators apply policies.

Pipelines coordinate evaluation.

End-to-End flows demonstrate the
complete architecture.

---

## Consequences

Future HAS platforms shall adopt
this architecture.

Architectural deviations require
a dedicated ADR.

