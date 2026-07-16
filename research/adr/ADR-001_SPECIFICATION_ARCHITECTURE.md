# ADR-001

Title

Separation of Specification Platform,
Conformance and Specification Runtime.

Status

Accepted

Date

2026-07

---

## Context

The HAS project is evolving from an
executable runtime into a specification-driven
runtime.

During this evolution it became evident that
three independent architectural concerns were
being treated as a single concept called
"Specification".

This coupling increases conceptual complexity
and makes future evolution difficult.

---

## Decision

The architecture shall explicitly separate
three independent layers.

Layer 1

Specification Platform (SP)

Responsible for:

- grammar

- style guide

- normative specification

- manifest

- specification consistency

Layer 2

Conformance

Responsible for proving that the
implementation conforms to the
normative specification.

Layer 3

Specification Runtime

Responsible for loading,
interpreting and executing
the specification.

---

## Resulting Roadmap

Phase I

Executable Runtime

↓

Phase II-A

Specification Platform

↓

Phase II-B

Conformance

↓

Phase III

Specification Runtime

↓

Phase IV

Executable Knowledge System

---

## Rationale

A specification is not the same as a
conformance process.

A conformance process is not the same as
a runtime capable of executing the
specification.

Separating these concerns reduces
architectural coupling and allows each
layer to evolve independently.

---

## Consequences

Future work shall be organized using the
following prefixes:

SP

Specification Platform

CONF

Conformance

SR

Specification Runtime

Only after Specification Platform and
Conformance reach maturity may the
Specification Runtime become the primary
source of truth for execution.

