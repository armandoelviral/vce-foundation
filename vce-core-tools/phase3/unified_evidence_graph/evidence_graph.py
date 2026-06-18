from phase3.unified_evidence_graph.evidence_node import (
    EvidenceNode,
)

from phase3.unified_evidence_graph.evidence_edge import (
    EvidenceEdge,
)


class EvidenceGraph:

    def __init__(self):

        self._nodes = {}
        self._edges = []

    def add_node(
        self,
        node: EvidenceNode,
    ) -> None:

        self._nodes[
            node.node_id
        ] = node

    def add_edge(
        self,
        edge: EvidenceEdge,
    ) -> None:

        self._edges.append(
            edge
        )

    def get_node(
        self,
        node_id: str,
    ):

        return self._nodes.get(
            node_id
        )

    def edges(
        self,
    ):

        return list(
            self._edges
        )

    def node_count(
        self,
    ) -> int:

        return len(
            self._nodes
        )

    def edge_count(
        self,
    ) -> int:

        return len(
            self._edges
        )
