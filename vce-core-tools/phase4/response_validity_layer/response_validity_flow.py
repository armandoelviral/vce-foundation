from phase4.response_validity_layer.response_capability import (
    ResponseCapability,
)

from phase4.response_validity_layer.response_validity_state import (
    ResponseValidityState,
)

from phase4.response_validity_layer.response_trust_verifier import (
    ResponseTrustVerifier,
)


class ResponseValidityFlow:

    @staticmethod
    def generate():

        capability = ResponseCapability(
            citizen_did="did:tcn:test:01",
            response_capable=True,
        )

        state = ResponseValidityState(
            citizen_did="did:tcn:test:01",
            response_state="RECOVERED",
        )

        trusted = (
            ResponseTrustVerifier.verify(
                state
            )
        )

        return {
            "capability":
                capability.to_dict(),
            "state":
                state.to_dict(),
            "trusted":
                trusted,
        }
