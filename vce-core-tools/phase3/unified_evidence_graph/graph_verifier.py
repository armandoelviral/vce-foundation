from phase3.unified_evidence_graph.evidence_graph import (
    EvidenceGraph,
)


class GraphVerifier:

    @staticmethod
    def verify(
        graph: EvidenceGraph,
    ) -> bool:

        for edge in graph.edges():

            source = graph.get_node(
                edge.source_id
            )

            target = graph.get_node(
                edge.target_id
            )

            if source is None:
                return False

            if target is None:
                return False

        return True
