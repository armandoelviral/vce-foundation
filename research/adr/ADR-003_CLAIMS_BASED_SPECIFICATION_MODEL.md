# ADR-003

Title

Claims-Based Specification Model

Status

Accepted

---

## Context

The Specification Platform originally treated
documents as the primary verification unit.

During SP-001 it became evident that
executable contracts do not verify entire
documents.

They verify individual normative statements.

---

## Decision

The primary verification unit of HAS shall be
the Claim.

Documents organize Claims.

Executable Contracts verify Claims.

Conformance demonstrates that the
implementation satisfies the verified Claims.

---

## Resulting Architecture

Document

↓

Claim

↓

Executable Contract

↓

Implementation

↓

Conformance

---

## Consequences

Traceability shall be established between:

Claim

↓

Executable Contract

↓

Implementation

rather than between complete documents and
implementations.

