class FailureDetector:

    def detect(self, membership):

        failures = []

        for node_id, data in membership.members.items():

            if not data["alive"]:

                failures.append(
                    {
                        "node_id": node_id,
                        "peer": data["peer"],
                        "status": "FAILED"
                    }
                )

        return failures
