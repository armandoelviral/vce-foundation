import requests


class StatePull:

    def pull(
        self,
        peer
    ):

        response = requests.get(
            f"{peer}/state",
            timeout=2
        )

        return response.json()
