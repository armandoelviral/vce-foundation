from phase3.unified_evidence_graph.evidence_graph import (
    EvidenceGraph,
)


class EvidenceTraversal:

    def __init__(
        self,
        graph: EvidenceGraph,
    ):

        self.graph = graph

    def neighbors(
        self,
        node_id: str,
    ):

        results = []

        for edge in self.graph.edges():

            if edge.source_id == node_id:

                node = self.graph.get_node(
                    edge.target_id
                )

                if node is not None:

                    results.append(
                        node
                    )

        return results
