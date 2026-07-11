# Canonical Event Contracts

Version: 1.0

Status: Draft

Classification: Contracts

---

# Purpose

Define the immutable structure shared by every Domain Event.

Platform technologies may change.

Contracts shall remain stable.

---

# Canonical Event

Every event contains:

event_id

event_type

aggregate_type

aggregate_id

occurred_at

producer

schema_version

tenant_id

correlation_id

causation_id

actor

payload

metadata

signature

---

# Rules

Events are immutable.

Events are append-only.

Events are versioned.

Events never contain behavior.

Events describe facts.

---

# Compatibility

Breaking changes require:

new schema version

migration policy

compatibility report

---

# Integrity

Every event shall be hashable.

Every event may be signed.

Every event shall be replayable.
