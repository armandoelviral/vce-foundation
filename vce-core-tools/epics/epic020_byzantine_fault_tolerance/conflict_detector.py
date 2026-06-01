class ConflictDetector:

    def __init__(self):

        self.history = {}


    def observe(
        self,
        vote
    ):

        key = (
            vote["node_id"],
            vote["artifact_hash"]
        )


        decision = vote[
            "decision"
        ]


        if key in self.history:

            if (
                self.history[key]
                !=
                decision
            ):

                return {
                    "conflict": True,
                    "node_id": vote[
                        "node_id"
                    ]
                }


        self.history[
            key
        ] = decision


        return {
            "conflict": False
        }
