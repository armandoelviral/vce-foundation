class NodeSimulator:

    def create_vote(
        self,
        node_id,
        artifact_hash,
        malicious=False
    ):

        if malicious:

            return {
                "node_id": node_id,
                "artifact_hash": artifact_hash,
                "decision": "INVALID",
                "behavior": "BYZANTINE"
            }


        return {
            "node_id": node_id,
            "artifact_hash": artifact_hash,
            "decision": "APPROVE",
            "behavior": "HONEST"
        }
