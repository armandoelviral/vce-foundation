# VCE Foundation Core Glossary v1.0

**Author:** Armando Miguel Elvira López (2026)

**Classification:** VCE Foundation Canonical Vocabulary

---

# I. Category Layer

## Computational Proof Management (CPM)

The organizational discipline responsible for governing, measuring, generating, preserving, and validating computational evidence across critical business processes.

CPM serves as the umbrella category under which standards, metrics, operations, certifications, and implementations are organized.

---

## Verifiable Computational Evidence (VCE)

A cryptographically verifiable proof that a computational process executed according to a defined specification.

VCE represents the technical standard underpinning Computational Proof Management.

---

# II. Core Metrics

## Computational Proof Score (CPS)

A maturity metric ranging from 0 to 5 that measures an organization's level of computational demonstrability.

| Level | Description                       |
| ----- | --------------------------------- |
| 0     | Assertions Only                   |
| 1     | Logs                              |
| 2     | Signed Logs                       |
| 3     | Provenance                        |
| 4     | Replayable Provenance             |
| 5     | Verifiable Computational Evidence |

---

## Evidence Coverage Ratio (ECR)

The percentage of critical organizational processes covered by demonstrable evidence mechanisms.

Range:

0% – 100%

---

## Evidence Debt Index (EDI)

A dimensionless measurement representing the accumulated risk created by insufficient computational proof coverage.

Higher EDI values indicate greater organizational exposure.

---

## Estimated Evidence Exposure (EEE)

A financial estimation of exposure resulting from evidence gaps.

EEE is expressed in monetary units and is intended for risk modeling rather than certification decisions.

---

# III. Operational Layer

## Evidence Operations (EvOps)

The operational discipline responsible for generating, validating, managing, preserving, and auditing evidence across production systems.

EvOps transforms CPM principles into day-to-day execution practices.

---

# IV. Evidence Objects

## Proof Session

A bounded execution context capable of generating verifiable evidence.

A Proof Session represents a single observable computational event or workflow.

---

## VCE Artifact

The minimum verifiable unit of computational evidence.

Each artifact contains the required VCE layers necessary to demonstrate execution integrity.

Core Layers:

* Identity
* Trust
* Provenance
* Evidence

Extended Layers:

* Replay
* Governance

---

## Evidence Graph

A directed acyclic graph (DAG) describing relationships between VCE Artifacts.

The graph captures lineage, dependency chains, and historical evidence relationships.

---

## Evidence Ledger

An append-only, tamper-evident persistence layer responsible for preserving evidence continuity over time.

The ledger maintains cryptographic linkage between sequential evidence records.

---

# V. Certification Layer

## VCE Bronze

Requirements:

* CPS ≥ 3

---

## VCE Silver

Requirements:

* CPS ≥ 4
* ECR ≥ 70%

---

## VCE Gold

Requirements:

* CPS ≥ 5
* ECR ≥ 90%

---

# Guiding Principle

Trust does not scale.

Evidence does.

