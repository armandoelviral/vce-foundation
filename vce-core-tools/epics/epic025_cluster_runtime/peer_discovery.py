import requests


class PeerDiscovery:

    def discover(self, peers):

        discovered = []

        for peer in peers:

            try:

                response = requests.get(
                    f"{peer}/state",
                    timeout=2
                )

                state = response.json()

                discovered.append(
                    {
                        "peer": peer,
                        "node_id": state["node_id"],
                        "alive": True
                    }
                )

            except Exception:

                discovered.append(
                    {
                        "peer": peer,
                        "alive": False
                    }
                )

        return discovered
