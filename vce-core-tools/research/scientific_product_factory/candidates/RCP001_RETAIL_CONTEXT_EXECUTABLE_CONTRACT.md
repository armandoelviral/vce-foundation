# RCP-001 Retail Context Executable Contract

Identifier

RCP-001-EC-01.

Version

0.1.

Status

CANDIDATE.

Authority

NONE.

Parent

RCP-001
Retail Context Profile.

Implementation

NOT AUTHORIZED
BY THIS RECORD.

Promotion

PROHIBITED.

---

## Purpose

Define the minimum
executable contract

for representing

a versioned,

immutable,

customer-configurable

Retail Context Profile

associated with

an existing SP001 Case.

The contract

shall represent

the commercial reality

declared applicable

to a specific

point of sale,

department,

fixture,

campaign,

or execution case.

The contract

shall not impose

one universal
Retail operating model.

---

## Architectural Location

The Retail Context Profile

belongs exclusively

to the Retail Vertical Pack.

It shall not be introduced

into:

VCE Core.

HAS Core.

CKP-006 Runtime
Execution Context.

The existing

SP001 Case

remains the generic
commercial workflow anchor.

Retail context

specializes the case

without replacing

the generic
Scientific Product
Domain Model.

---

## Snapshot Rule

A Retail Context Profile

shall initially exist

as an immutable

versioned snapshot.

A contextual change

shall produce

a new snapshot version.

It shall not silently

mutate

an existing snapshot.

The snapshot

shall not require

an independent

long-lived aggregate

or a complex
standalone lifecycle.

---

## Minimum Snapshot Identity

Every Retail Context
Snapshot

shall identify:

Snapshot Identifier.

Snapshot Version.

Associated Case Identifier.

Customer Context
Definition Identifier.

Declared Context Scope.

Snapshot Provenance.

The contract

shall not infer

missing identity

from filenames,

fixture names,

category counts,

or commercial narratives.

---

## Customer Context Definition

A customer

may declare

which contextual dimensions

are applicable

to its operation.

Different customers

may require

different dimensions.

Different cases

for the same customer

may require

different context scopes.

A contextual dimension

shall not become

universally mandatory

solely because

it appeared

in another
commercial case.

---

## Context Dimension Record

Each declared dimension

shall preserve:

Dimension Identifier.

Dimension Type.

Applicability Status.

Evidence Status.

Declared Value

when available.

Value Provenance.

Evidence Reference

when available.

Interpretation Boundary.

A missing value

shall remain explicit.

An unavailable value

shall not be synthesized.

An inapplicable dimension

shall not be treated

as missing evidence.

---

## Initial Dimension Vocabulary

Candidate dimension types

include:

FLOOR_AREA.

DEPARTMENT.

FIXTURE_TYPE.

PRESENTATION_CAPACITY.

ACTIVE_CATEGORY.

PURCHASE_VOLUME.

COMMERCIAL_CLUSTER.

APPLICABLE_FIXTURE.

Additional dimensions

may be declared

by a customer

without changing

VCE Core,

HAS Core,

or the generic

SP001 Case model.

The initial vocabulary

does not assert

cross-customer universality.

---

## Dimension Applicability

Allowed applicability values:

REQUIRED.

OPTIONAL.

NOT_APPLICABLE.

DISPUTED.

REQUIRED

means a dimension

is necessary

for the declared case

or a specific
dependent evaluation.

OPTIONAL

means a dimension

may provide
additional context

without being mandatory.

NOT_APPLICABLE

means the customer

or case

does not require

that dimension.

DISPUTED

means the contextual
interpretation

cannot be resolved

from current evidence.

---

## Dimension Evidence Status

Allowed evidence states:

DOCUMENTED.

HUMAN_DECLARED.

MEASURED.

INDEPENDENTLY_VERIFIED.

NOT_PROVIDED.

INSUFFICIENT_EVIDENCE.

DISPUTED.

A human declaration

shall not be presented

as independently verified.

A source discrepancy

shall not be erased

to create

apparent consistency.

External confidential
evidence

shall remain outside

the repository.

Only approved

opaque identifiers,

hashes,

and sanitized references

may be retained.

---

## Value Representation

Dimension values

shall be represented

according to

their declared type.

Examples:

Floor area

may be represented

as a numeric quantity

with a declared unit.

Department

may be represented

as an opaque identifier

or customer-approved
classification.

Fixture type

may be represented

as a customer-defined
fixture classification.

Capacity

may be represented

as an explicitly
declared count,

range,

or unavailable value.

The contract

shall not assume

all customers

share the same taxonomy,

units,

labels,

or merchandising rules.

---

## Case Association

A Retail Context Snapshot

shall associate

with an existing

SP001 Case.

The association

shall preserve

the Case identity.

It shall not require

Retail-specific fields

inside generic

Objective,

Case,

Recommendation,

Expert Decision,

or Operational Evidence

contracts.

A Retail adapter,

extension,

or scoped association

may connect

the snapshot

to the Case.

The concrete mechanism

remains pending

implementation design

and test evidence.

---

## Evaluation Dependency Rule

A constraint

may declare

which contextual dimensions

it requires.

If a required dimension

is unavailable,

the affected evaluation

shall return

INSUFFICIENT_EVIDENCE.

Other evaluations

with sufficient evidence

may continue.

The entire case

shall not automatically fail

because an unrelated

optional dimension

is unavailable.

A dimension marked

NOT_APPLICABLE

shall not be interpreted

as an evidence failure.

A disputed dimension

shall preserve

its uncertainty

in dependent evaluations.

---

## Fixture Independence Rule

Active categories

shall not be equated

with fixture count.

Departments

shall not be equated

with fixture count.

Floor area

shall not be treated

as proof

of installed fixture count.

Presentation capacity

shall not be invented

from product category,

store format,

or channel name.

Applicable fixture counts

require independent

declared,

documented,

or measured evidence.

---

## Customer Variability Rule

A selling floor

shall not be presumed

identical

to another selling floor

solely because

both belong

to the same channel,

cluster,

brand,

or campaign.

A customer-defined

context profile

may vary by:

Point of sale.

Department.

Campaign.

Delivery.

Fixture.

Commercial segment.

Operational requirement.

Cross-store projection

requires explicit

supporting evidence.

---

## Commercial Boundaries

A context snapshot

does not establish:

Customer acceptance.

Commercial savings.

Revenue.

Conversion uplift.

Labor reduction.

Willingness to pay.

Fixture compliance.

Authority to implement.

Those outcomes

require independent

commercial,

operational,

or contractual evidence.

---

## Minimum Executable Test Conditions

Future implementation

shall demonstrate:

Snapshot identity

is explicit.

Snapshot version

is explicit.

Snapshot values

cannot be silently mutated.

The snapshot

associates with

an existing SP001 Case.

Different customers

can require

different dimension sets.

Missing required dimensions

remain explicit.

Optional dimensions

do not block

unrelated evaluations.

NOT_APPLICABLE dimensions

are not treated

as missing evidence.

Disputed dimensions

preserve uncertainty.

Fixture counts

are not inferred

from category counts.

Retail semantics

do not enter

VCE Core.

Retail semantics

do not enter

HAS Core.

Retail semantics

do not alter

CKP-006 runtime context.

Confidential evidence

does not enter

the repository.

---

## Current Disposition

Contract Status

CANDIDATE.

Customer Flexibility

REQUIRED.

Universal Retail Schema

NOT ESTABLISHED.

Retail Context Snapshot

VERSIONED
AND IMMUTABLE.

Existing SP001 Workflow

PRESERVED.

Implementation Authorization

NOT GRANTED.

Commercial Outcome

NOT ESTABLISHED.

Promotion

PROHIBITED.

---

## Next Required Activity

Inspect the existing

SP001 package boundaries,

project configuration,

test discovery,

and extension locations.

Identify the minimum

Retail-specific

snapshot contract

and its association

with an existing Case.

Propose one bounded

test-first

implementation slice

without modifying

VCE Core,

HAS Core,

or CKP-006.

---

# End of RCP-001-EC-01
