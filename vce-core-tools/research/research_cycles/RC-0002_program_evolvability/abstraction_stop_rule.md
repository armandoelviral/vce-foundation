# Abstraction Stop Rule

## Purpose

Prevent infinite abstraction during RC-0002.

The Research Program shall not introduce higher-level abstractions unless they demonstrably reduce total architectural complexity.

---

## Rule ASR-001

A new abstraction may be introduced only if it eliminates, unifies or simplifies existing mechanisms without reducing explanatory capability.

---

## Rule ASR-002

A new abstraction shall be rejected if it only increases generality without reducing the number of mechanisms, concepts or dependencies.

---

## Rule ASR-003

The preferred stopping point is the lowest abstraction level that preserves explanatory completeness.

---

## Application to Reduction

Reduction shall remain the current candidate mechanism unless a higher-level abstraction demonstrably reduces total architectural complexity.

---

## Decision Rule

Do not abstract upward unless abstraction produces measurable simplification.
