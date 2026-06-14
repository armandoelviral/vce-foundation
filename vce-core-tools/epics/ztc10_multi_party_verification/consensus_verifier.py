from epics.ztc10_multi_party_verification.witness_registry import (
    WitnessRegistry,
)

from epics.ztc10_multi_party_verification.witness_response import (
    WitnessResponse,
)


class ConsensusVerifier:

    @staticmethod
    def verify(
        response: WitnessResponse,
        registry: WitnessRegistry,
    ) -> bool:

        if not registry.exists(
            response.witness_id
        ):
            return False

        if not response.accepted:
            return False

        return True
