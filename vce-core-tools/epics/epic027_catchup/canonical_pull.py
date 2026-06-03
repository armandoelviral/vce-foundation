import requests


class CanonicalPull:

    def pull(
        self,
        peer
    ):

        response = requests.get(
            f"{peer}/state",
            timeout=2
        )

        state = response.json()

        return {
            "peer": peer,
            "ledger": state["ledger"]
        }
