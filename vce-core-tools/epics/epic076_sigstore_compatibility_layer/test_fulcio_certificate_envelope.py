from epics.epic076_sigstore_compatibility_layer.fulcio_certificate import (
    FulcioCertificateEnvelope,
)
from epics.epic076_sigstore_compatibility_layer.oidc_identity import (
    OIDCIdentityEnvelope,
)


def build_oidc_identity():

    return OIDCIdentityEnvelope(
        issuer="https://token.actions.githubusercontent.com",
        subject="repo:org/project",
        workflow_identity="release.yml",
        runner_identity="github-hosted",
        repository_identity="org/project",
    )


def test_fulcio_certificate_envelope_creation():

    certificate = FulcioCertificateEnvelope(
        certificate_subject="repo:org/project",
        certificate_issuer="Fulcio",
        certificate_not_before="2026-06-09T00:00:00Z",
        certificate_not_after="2026-06-09T00:10:00Z",
        public_key_binding="public-key-hash",
        oidc_identity=build_oidc_identity(),
    )

    assert certificate.certificate_issuer == "Fulcio"


def test_fulcio_certificate_binds_oidc_identity():

    certificate = FulcioCertificateEnvelope(
        certificate_subject="repo:org/project",
        certificate_issuer="Fulcio",
        certificate_not_before="2026-06-09T00:00:00Z",
        certificate_not_after="2026-06-09T00:10:00Z",
        public_key_binding="public-key-hash",
        oidc_identity=build_oidc_identity(),
    )

    as_dict = certificate.to_dict()

    assert as_dict["oidc_identity"]["issuer"] == (
        "https://token.actions.githubusercontent.com"
    )
    assert as_dict["oidc_identity"]["repository_identity"] == "org/project"


def test_fulcio_certificate_contains_public_key_binding():

    certificate = FulcioCertificateEnvelope(
        certificate_subject="repo:org/project",
        certificate_issuer="Fulcio",
        certificate_not_before="2026-06-09T00:00:00Z",
        certificate_not_after="2026-06-09T00:10:00Z",
        public_key_binding="public-key-hash",
        oidc_identity=build_oidc_identity(),
    )

    assert certificate.public_key_binding == "public-key-hash"
