"""Issue a commitment proof from the authority register's committed view."""

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from sp001.contracts.product001_mvp1_commitment_certificate import (
    CommitmentCertificateV1,
    CommitmentContextV1,
    commitment_signing_payload,
)
from sp001.contracts.product001_mvp1_contextual_authorization import (
    decision_digest_from_canonical_bytes,
)
from sp001.infrastructure.sqlite_product001_mvp1_authorization_store import (
    SqliteMvp1AuthorizationStore,
)


class Mvp1CommitmentIssuer:
    """Internal authority service with an independently provisioned signing key."""

    def __init__(
        self, *, store: SqliteMvp1AuthorizationStore, signing_key: Ed25519PrivateKey,
    ):
        if not isinstance(store, SqliteMvp1AuthorizationStore):
            raise TypeError("authority store required")
        if not isinstance(signing_key, Ed25519PrivateKey):
            raise TypeError("commitment signing key required")
        self._store = store
        self._signing_key = signing_key

    def issue(
        self, *, organization_id: str, operation_id: str, authorization_digest: str,
    ) -> CommitmentCertificateV1 | None:
        """Return the same proof on recovery, including its original deadline."""
        intent = self._store.recover(
            organization_id=organization_id,
            operation_id=operation_id,
            expected_digest=authorization_digest,
        )
        if intent is None:
            return None
        context = CommitmentContextV1(
            issuer_id=intent.issuer_id,
            organization_id=intent.organization_id,
            operation_id=intent.operation_id,
            authorization_digest=intent.authorization_digest,
            decision_digest=decision_digest_from_canonical_bytes(intent.decision_bytes),
            materialize_deadline=intent.materialize_deadline,
        )
        return CommitmentCertificateV1(
            context, self._signing_key.sign(commitment_signing_payload(context)),
        )
