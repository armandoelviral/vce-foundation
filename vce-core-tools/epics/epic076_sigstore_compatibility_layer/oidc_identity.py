from dataclasses import dataclass


@dataclass(frozen=True)
class OIDCIdentityEnvelope:

    issuer: str

    subject: str

    workflow_identity: str

    runner_identity: str

    repository_identity: str
