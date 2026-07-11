# Bounded Contexts

Version: 0.1

Status: Draft

Classification: Architecture

---

# Purpose

Define the independent domains composing the Institutional Capability Platform.

Each context owns a specific responsibility.

Contexts collaborate.

Contexts never duplicate responsibilities.

---

# Context 1

Human Expertise

Purpose

Capture expert reasoning.

Responsibilities

- Expert decisions
- Decision rationale
- Experience capture
- Strategic intent
- Exception justification

Produces

Human Knowledge Events

---

# Context 2

Decision Intelligence

Purpose

Generate recommendations.

Responsibilities

- AI
- Optimization
- Simulation
- Recommendation generation

Consumes

Human Expertise

Operational Evidence

Produces

Recommendations

---

# Context 3

Operational Evidence

Purpose

Capture real-world execution.

Responsibilities

- Compliance
- Sales
- KPIs
- Execution
- Outcomes

Produces

Evidence Events

---

# Context 4

Institutional Memory

Purpose

Persist organizational knowledge.

Responsibilities

- Decision history
- Evidence
- Policies
- Expert reasoning
- Longitudinal history

Produces

Knowledge Graph updates

---

# Context 5

Governance

Purpose

Validate organizational knowledge.

Responsibilities

- Review
- Promotion
- Policy approval
- Capability approval

Produces

Institutional Policies

---

# Context 6

Capability Management

Purpose

Manage organizational capabilities.

Responsibilities

- Capability lifecycle
- Capability metrics
- Capability evolution

Produces

Institutional Capability Registry

---

# Context 7

Workflow Orchestration

Purpose

Coordinate all platform processes.

Responsibilities

- Process orchestration
- State transitions
- Event routing

---

# Context 8

Asset Platform

Purpose

Manage reusable organizational assets.

Responsibilities

- Generic Assets
- User Assets
- Brand Assets
- Fixture Assets
- Templates

---

# Context 9

Identity & Security

Purpose

Protect organizational integrity.

Responsibilities

- Authentication
- Authorization
- Audit
- Traceability

---

# Context Rule

Each bounded context owns exactly one business capability.

No capability may belong to multiple contexts.

Collaboration occurs exclusively through governed events.
