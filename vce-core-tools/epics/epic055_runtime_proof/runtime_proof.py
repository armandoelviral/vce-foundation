from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeProof:

    snapshot: object

    attestation: object

    provenance: object
