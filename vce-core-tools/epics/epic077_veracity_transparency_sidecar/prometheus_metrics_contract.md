# EPIC077-D7 — Prometheus Metrics Contract

## Goal

Define the Prometheus metrics emitted by the Veracity Transparency Sidecar.

## Required Metrics

### veracity_anchor_jobs_total

Type:

- counter

Description:

- Total number of transparency anchor jobs created.

### veracity_anchor_success_total

Type:

- counter

Description:

- Total number of transparency anchor jobs completed successfully.

### veracity_anchor_failure_total

Type:

- counter

Description:

- Total number of transparency anchor jobs that failed.

### veracity_anchor_retry_total

Type:

- counter

Description:

- Total number of transparency anchor retries.

### veracity_pending_jobs

Type:

- gauge

Description:

- Current number of pending transparency anchor jobs.

### veracity_anchor_latency_seconds

Type:

- histogram

Description:

- Transparency anchoring latency in seconds.

### veracity_rekor_set_total

Type:

- counter

Description:

- Total number of Rekor Signed Entry Timestamps received.

## Required Labels

Metrics may include:

- backend
- status
- namespace
- pod
- error_code

## Required Properties

Metrics must be:

- scrapeable by Prometheus
- stable across sidecar versions
- low cardinality
- suitable for Grafana dashboards
