# ADR-021: Browser-Based Independent Verification

## Status

Accepted

## Context

The Zero-Trust Compute architecture currently supports trusted artifacts, deterministic execution, replay, attestations, transparency logs, and quantum-resilient evidence.

However, most verification flows still assume that an auditor interacts with backend infrastructure controlled by the platform operator.

For high-trust environments, this is insufficient.

An external auditor should be able to verify an evidence artifact independently, using a local browser runtime, without trusting the original backend that produced the attestation.

## Decision

The system will support a browser-based independent verification portal.

The portal will allow an auditor to:

- Upload or paste a D5 evidence artifact.
- Verify the artifact hash locally.
- Verify transparency-layer anchoring.
- Retrieve or validate the referenced historical WASM artifact.
- Re-execute the deterministic policy locally in a WebAssembly sandbox.
- Recompute the resulting state root.
- Compare the recomputed state root against the historical attested result.
- Display a final verification verdict.

## Verification Flow

```text
D5 Evidence Artifact
        ↓
Browser Auditor Portal
        ↓
Local Hash Verification
        ↓
Transparency Layer Check
        ↓
Historical WASM Retrieval
        ↓
Local WASM Replay
        ↓
State Root Recalculation
        ↓
Attested Result Comparison
        ↓
Independent Verification Verdict

## Security Requirements

The browser verifier must not trust server-side claims without local validation.

The verifier must eventually support:

```text
WebCrypto SHA-256
Ed25519 verification
Hybrid signature envelope verification
Merkle inclusion proof verification
WASM replay
State root comparison
```
The verifier must reject evidence if any of the following fail:

```text
Invalid JSON structure
Invalid artifact hash
Invalid signature
Missing transparency proof
Failed replay
Mismatched state root
Unsupported policy version

## Non-Goals

This ADR does not implement the browser portal.

This ADR does not replace server-side verification.

This ADR does not define the full UI design.

This ADR does not introduce multi-party consensus.

## Consequences

This creates a product-facing audit surface for Zero-Trust Compute.

It also enables external auditors, regulators, customers, and independent witnesses to verify computations without privileged backend access.

This directly strengthens:

ZTC-3 Trusted Replay
ZTC-5 Trusted Transparency
ZTC-6 Execution Provenance Binding
ZTC-7 Quantum-Resilient Evidence
ZTC-10 Multi-Party Verification

## Future Work

A future implementation track should introduce:

```text
ZTC-12 Browser Verification Portal

D5 Evidence Upload
WebCrypto Hashing
Signature Verification
Transparency Proof Validation
WASM Sandbox Replay
Replay Result Visualization
Final Audit Verdict

