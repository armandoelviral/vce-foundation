from phase3.governance_inclusion_proof.proof_registry import (
    ProofRegistry,
)


class ProofQuery:

    def __init__(
        self,
        registry: ProofRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        proof_id: str,
    ):

        return self.registry.get(
            proof_id
        )
