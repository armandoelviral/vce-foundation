# HAS Capability Coverage Model

Version

1.0

Status

Draft

---

## Purpose

Define how Capability Coverage is computed.

Coverage evaluates whether every
registered Capability possesses the
required executable evidence.

---

## Coverage Rule

Capability

↓

Claim

↓

Executable Contract

↓

Covered

---

## Covered

A Capability is Covered when:

- every referenced Claim exists;

- every referenced Contract exists.

---

## Not Covered

A Capability is Not Covered if one or more
Claims or Contracts cannot be resolved.

---

## Output

Coverage Percentage.

Covered Capabilities.

Missing Claims.

Missing Contracts.

