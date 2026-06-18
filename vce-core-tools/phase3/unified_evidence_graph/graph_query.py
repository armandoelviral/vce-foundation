from phase3.unified_evidence_graph.evidence_graph import (
    EvidenceGraph,
)


class GraphQuery:

    def __init__(
        self,
        graph: EvidenceGraph,
    ):

        self.graph = graph

    def node(
        self,
        node_id: str,
    ):

        return self.graph.get_node(
            node_id
        )
