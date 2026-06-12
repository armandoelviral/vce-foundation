# EPIC084-D1 Witness Consensus Contract

## Goal

Determine whether a ledger root has been independently observed by a sufficient number of external witnesses.

## Core Principle

A single witness provides observation.

Multiple independent witnesses provide consensus.

## Required Inputs

- ledger_root
- witness_receipts
- consensus_policy

## Required Outputs

- CONSENSUS_ACHIEVED
- CONSENSUS_NOT_ACHIEVED

## Required Properties

The system must support:

- multiple witnesses
- independent verification
- configurable thresholds
- deterministic evaluation

## Example Policies

- 1 of 1
- 2 of 3
- 3 of 5
- 5 of 7

## Non Goals

Consensus does not prove correctness of evidence.

Consensus proves independent observation of the ledger root.
