class NetworkConvergence:

    def verify(
        self,
        node_states
    ):

        if not node_states:

            return {
                "converged": False,
                "reason": "EMPTY_NETWORK"
            }


        hashes = set(
            node_states.values()
        )


        return {
            "converged":
                len(hashes) == 1,

            "nodes":
                len(node_states),

            "unique_states":
                len(hashes)
        }
