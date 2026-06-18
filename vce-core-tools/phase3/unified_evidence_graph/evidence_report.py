from phase3.unified_evidence_graph.evidence_graph import (
    EvidenceGraph,
)


class EvidenceReport:

    def __init__(
        self,
        graph: EvidenceGraph,
    ):

        self.graph = graph

    def node_count(
        self,
    ) -> int:

        return self.graph.node_count()

    def edge_count(
        self,
    ) -> int:

        return self.graph.edge_count()

    def to_dict(
        self,
    ):

        return {
            "node_count":
                self.node_count(),
            "edge_count":
                self.edge_count(),
        }
