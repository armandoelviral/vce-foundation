# ADR-022: Multi-Cloud Witness Deployment

## Status

Accepted

## Context

ZTC-10 introduces multi-party verification through independent witness nodes.

A witness should not only be a logical verifier. For high-assurance deployments, each witness should run in an independent infrastructure trust domain.

If all witnesses run in the same cloud account, region, provider, or administrative boundary, a single infrastructure compromise could affect quorum integrity.

## Decision

The system will support a multi-cloud witness deployment model.

A reference topology MAY deploy witnesses across independent providers such as:

```text
Witness 01 -> AWS
Witness 02 -> Google Cloud
Witness 03 -> Microsoft Azure
```

## Reference Topology

```text
Client Application
        |
        v
Consensus Coordinator
        |
        +-------------------+-------------------+
        |                   |                   |
        v                   v                   v
   AWS Witness          GCP Witness        Azure Witness
        |                   |                   |
   KMS / HSM           Cloud KMS          Key Vault / HSM
        |                   |                   |
        +-------------------+-------------------+
                            |
                    M-of-N Quorum
                            |
                            v
                 Consensus Evidence Artifact
                            |
                            v
                   Transparency Layer
```

## Security Requirements

Witness nodes should be deployed across separate infrastructure trust domains.

The coordinator should communicate with witnesses using authenticated encrypted transport.

The witness network model should avoid east-west witness-to-witness communication.

A witness response must not count toward quorum unless:

```text
The witness is registered
The witness identity is valid
The response is accepted
The state root is present
The required signatures are present
The response belongs to the expected computation
```

A cloud-provider outage should degrade quorum availability but must not silently downgrade verification guarantees.

## Operational Requirements

The reference deployment MAY be automated using Infrastructure as Code.

A multi-cloud deployment should emit coordinator-ready witness endpoints.

The deployment should preserve:

```text
provider separation
regional separation
restricted ingress
minimal egress
key custody separation
witness identity metadata
```

## Non-Goals

This ADR does not require every deployment to use three clouds.

This ADR does not mandate AWS, GCP, or Azure specifically.

This ADR does not claim automatic regulatory compliance.

This ADR does not implement Terraform modules.

This ADR does not define production-grade IAM, logging, patching, or incident response.

## Consequences

This strengthens ZTC-10 Multi-Party Verification by turning witnesses into independent trust domains.

It also prepares ZTC-11 Distributed Attestation.

The main operational tradeoff is increased infrastructure complexity.

Infrastructure as Code can reduce deployment friction, but it does not eliminate multi-cloud operational responsibility.

## Future Work

Future implementation tracks may introduce:

```text
Terraform reference deployment
Witness endpoint registry generation
mTLS certificate provisioning
Cloud KMS signing adapters
PQC signing adapters
Witness health checks
Quorum availability monitoring
```
