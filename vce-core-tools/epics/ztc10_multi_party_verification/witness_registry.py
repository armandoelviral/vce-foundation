from epics.ztc10_multi_party_verification.witness_contract import (
    WitnessContract,
)


class WitnessRegistry:

    def __init__(self):
        self.witnesses = {}

    def register(
        self,
        witness: WitnessContract,
    ) -> None:

        self.witnesses[witness.witness_id] = witness

    def exists(
        self,
        witness_id: str,
    ) -> bool:

        return witness_id in self.witnesses
