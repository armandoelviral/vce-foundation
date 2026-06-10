# EPIC077-D11 — Privacy-Preserving Data Flow Contract

## Goal

Define the privacy-preserving data flow between the core application container and the Veracity Transparency Sidecar.

## Core Rule

Raw sensitive data must never be written to the shared sidecar volume.

Sensitive data includes:

- PHI
- PII
- biometrics
- raw transaction payloads
- raw medical payloads

## Core Container Responsibilities

The core application container may access raw sensitive data.

It must only emit:

- salted HMAC-SHA256 footprints
- logical metadata
- execution identifiers
- artifact references
- Veracity pipeline state traces

## Shared Volume Policy

The shared volume may contain:

- pipe.log
- hashes
- metadata
- anchor jobs
- status updates

The shared volume must not contain:

- raw PHI
- raw PII
- raw biometrics
- raw medical records
- raw financial payloads

## Sidecar Responsibilities

The Veracity Transparency Sidecar must:

- read pending proof traces
- construct anchor jobs
- process jobs asynchronously
- submit transparency evidence
- update anchor status
- emit Prometheus metrics

The sidecar must not require access to raw sensitive data.

## Required Property

The transparency sidecar can complete anchoring without reading raw sensitive payloads.
