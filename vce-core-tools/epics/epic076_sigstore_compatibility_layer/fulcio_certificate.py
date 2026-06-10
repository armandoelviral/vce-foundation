from dataclasses import dataclass

from epics.epic076_sigstore_compatibility_layer.oidc_identity import (
    OIDCIdentityEnvelope,
)


@dataclass(frozen=True)
class FulcioCertificateEnvelope:
    certificate_subject: str
    certificate_issuer: str
    certificate_not_before: str
    certificate_not_after: str
    public_key_binding: str
    oidc_identity: OIDCIdentityEnvelope

    def to_dict(self):

        return {
            "certificate_subject": self.certificate_subject,
            "certificate_issuer": self.certificate_issuer,
            "certificate_not_before": self.certificate_not_before,
            "certificate_not_after": self.certificate_not_after,
            "public_key_binding": self.public_key_binding,
            "oidc_identity": {
                "issuer": self.oidc_identity.issuer,
                "subject": self.oidc_identity.subject,
                "workflow_identity": self.oidc_identity.workflow_identity,
                "runner_identity": self.oidc_identity.runner_identity,
                "repository_identity": self.oidc_identity.repository_identity,
            },
        }
