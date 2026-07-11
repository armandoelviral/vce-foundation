# Core and Vertical Boundary

Version: 0.1

Status: Draft

Classification: Architecture

---

## Purpose

Define the boundary between the domain-independent Institutional Capability Platform and domain-specific Vertical Packs.

The Core provides reusable capabilities.

Vertical Packs provide domain semantics, workflows, assets and policies.

---

# Domain-Independent Core

## Workflow Orchestration

Coordinates governed workflows, state transitions, retries and event routing.

The Core shall not contain Retail-specific workflow semantics.

---

## Asset Platform

Provides:

- asset identity;
- versioning;
- lineage;
- storage;
- access control;
- integrity verification;
- reusable templates;
- portable project packages.

The Core does not define garments, fixtures or planograms.

---

## Institutional Memory

Preserves:

- decisions;
- rationale;
- evidence;
- outcomes;
- policies;
- capability history.

The Core stores governed reasoning independently of domain vocabulary.

---

## Knowledge Graph Platform

Provides:

- typed entities;
- governed relationships;
- provenance;
- temporal history;
- evidence links;
- ontology extension.

The Core does not define Retail entities.

---

## Human Expertise Platform

Provides:

- recommendation review;
- acceptance;
- rejection;
- modification;
- rationale capture;
- expert attribution;
- candidate knowledge generation.

---

## Decision Intelligence Platform

Provides generic interfaces for:

- scoring;
- recommendation;
- optimization;
- simulation;
- explanation;
- confidence;
- policy evaluation.

Decision models remain pluggable.

---

## Evidence Platform

Provides:

- evidence records;
- expected-versus-observed comparison;
- longitudinal measurement;
- replay;
- audit trail;
- outcome attribution.

---

## Governance Platform

Provides:

- candidate review;
- policy promotion;
- approval;
- rejection;
- deprecation;
- capability institutionalization.

---

## Identity and Security Platform

Provides:

- authentication;
- authorization;
- tenancy;
- audit;
- cryptographic integrity;
- organizational boundaries.

---

## API Platform

Provides versioned contracts for all shared platform capabilities.

---

# Retail Vertical Pack

The Retail Pack owns all Retail-specific semantics.

## Retail Ontology

Defines:

- SKU;
- collection;
- brand;
- store;
- department;
- fixture;
- slot;
- facing;
- campaign;
- planogram;
- execution;
- compliance.

---

## Retail Context Engine

Interprets:

- commercial calendar;
- local market;
- climate;
- social context;
- store format;
- campaign;
- category;
- seasonality.

Produces Retail Context Scores.

---

## Retail Decision Engine

Consumes:

- inventory;
- sales;
- sell-through;
- margin;
- arrivals;
- brand rules;
- context;
- fixture capacity.

Produces explainable planogram recommendations.

---

## Retail Simulation Engine

Evaluates Retail scenarios such as:

- inventory arrival;
- climate change;
- promotion change;
- layout change;
- assortment change.

---

## Retail VM Composer

Produces deterministic visual representations of approved planograms.

It executes approved decisions.

It does not determine commercial strategy.

---

## Retail Execution Verification

Compares:

Planogram

↓

Observed Store Execution

↓

Compliance and Variance

---

## Retail Analytics

Defines Retail metrics including:

- GMROI;
- sell-through;
- inventory turn;
- facing productivity;
- space productivity;
- compliance.

---

## Retail Asset Extensions

Defines:

- garment assets;
- fixture profiles;
- calibrated templates;
- brand assets;
- campaign assets;
- store assets.

---

# Initial Retail Applications

## Retail VM Composer Pro

Primary authoring and decision-review environment.

---

## Retail VM Fixture Calibrator

Creates governed fixture calibration profiles.

A calibration profile may include:

- planar homography;
- multi-plane geometry;
- photometric calibration;
- lens correction;
- dimensional constraints;
- confidence;
- provenance;
- version.

---

## VM Cloud Assets

Retail-specific user experience over the shared Asset Platform.

---

# Boundary Rule

A component belongs to the Core only when it can support multiple domains without importing Retail semantics.

A component belongs to the Retail Vertical Pack when its behavior depends upon Retail vocabulary, rules, assets or metrics.

---

# Dependency Rule

Vertical Packs may depend upon Core capabilities.

The Core shall never depend upon a Vertical Pack.

---

# Validation Rule

A capability shall not be promoted to the Core merely because it appears reusable.

Reuse must be demonstrated in at least one additional domain or justified through an explicit architecture review.

---

# Closing Statement

Retail is the first reference implementation of the Institutional Capability Platform.

It validates the Core.

It does not define the Core.
