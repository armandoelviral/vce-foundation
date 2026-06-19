from phase3.governance_provenance.provenance_registry import (
    ProvenanceRegistry,
)


class ProvenanceQuery:

    def __init__(
        self,
        registry: ProvenanceRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        provenance_id: str,
    ):

        return self.registry.get(
            provenance_id
        )
