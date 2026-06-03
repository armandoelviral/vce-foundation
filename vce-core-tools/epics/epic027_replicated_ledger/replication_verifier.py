import requests


class ReplicationVerifier:

    def fetch_ledgers(self, peers):

        ledgers = {}

        for peer in peers:

            try:
                response = requests.get(
                    f"{peer}/state",
                    timeout=2
                )

                state = response.json()

                ledgers[peer] = state["ledger"]

            except Exception as e:
                ledgers[peer] = {
                    "error": str(e)
                }

        return ledgers


    def verify(self, ledgers):

        serialized = [
            str(ledger)
            for ledger in ledgers.values()
        ]

        return {
            "replicated": len(set(serialized)) == 1,
            "nodes": len(ledgers),
            "unique_ledgers": len(set(serialized))
        }
