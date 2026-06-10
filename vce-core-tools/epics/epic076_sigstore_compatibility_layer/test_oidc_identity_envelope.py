from epics.epic076_sigstore_compatibility_layer.oidc_identity import (
    OIDCIdentityEnvelope,
)


def test_oidc_identity_envelope_creation():

    identity = OIDCIdentityEnvelope(
        issuer="https://token.actions.githubusercontent.com",
        subject="repo:org/project",
        workflow_identity="build.yml",
        runner_identity="github-hosted",
        repository_identity="org/project",
    )

    assert identity.issuer.startswith(
        "https://"
    )


def test_oidc_identity_contains_required_fields():

    identity = OIDCIdentityEnvelope(
        issuer="issuer",
        subject="subject",
        workflow_identity="workflow",
        runner_identity="runner",
        repository_identity="repo",
    )

    assert identity.subject == "subject"

    assert identity.workflow_identity == "workflow"

    assert identity.runner_identity == "runner"

    assert identity.repository_identity == "repo"


def test_oidc_identity_is_immutable():

    identity = OIDCIdentityEnvelope(
        issuer="issuer",
        subject="subject",
        workflow_identity="workflow",
        runner_identity="runner",
        repository_identity="repo",
    )

    assert identity.issuer == "issuer"
