from types import SimpleNamespace

from phase4.constitutional_identity_layer.identity_right import (
    IdentityRight,
)

from phase4.constitutional_identity_layer.identity_registry import (
    IdentityRegistry,
)

from phase4.constitutional_identity_layer.identity_sovereignty import (
    IdentitySovereignty,
)

from phase4.constitutional_identity_layer.identity_revocation import (
    IdentityRevocation,
)

from phase4.constitutional_identity_layer.identity_recovery import (
    IdentityRecovery,
)

from phase4.constitutional_identity_layer.identity_continuity import (
    IdentityContinuity,
)

from phase4.constitutional_identity_layer.identity_verifier import (
    IdentityVerifier,
)


class IdentityFlow:

    @staticmethod
    def generate():

        right = IdentityRight(
            identity_id="identity-001",
            right_name="identity_ownership",
        )

        registry = IdentityRegistry(
            identities=[right]
        )

        sovereignty = IdentitySovereignty(
            identity_id="identity-001",
            sovereign=True,
        )

        revocation = IdentityRevocation(
            identity_id="identity-001",
            revoked=False,
        )

        recovery = IdentityRecovery(
            identity_id="identity-001",
            recovered=True,
        )

        continuity = IdentityContinuity(
            identity_id="identity-001",
            continuous=True,
        )

        identity = SimpleNamespace(
            sovereign=sovereignty.sovereign,
            revoked=revocation.revoked,
            continuous=continuity.continuous,
        )

        valid = IdentityVerifier.verify(
            identity
        )

        return {
            "right":
                right.to_dict(),
            "registry":
                registry.to_dict(),
            "sovereignty":
                sovereignty.to_dict(),
            "revocation":
                revocation.to_dict(),
            "recovery":
                recovery.to_dict(),
            "continuity":
                continuity.to_dict(),
            "valid":
                valid,
        }
