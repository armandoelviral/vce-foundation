import requests


class RecoveryHandshake:

    def request_cluster_state(
        self,
        peers
    ):

        states = []

        for peer in peers:

            try:

                state = requests.get(
                    f"{peer}/state",
                    timeout=2
                ).json()

                states.append(state)

            except Exception:

                pass

        return states
