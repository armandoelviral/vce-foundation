import requests


class BroadcastAppend:

    def broadcast(self, peers, event):

        results = []

        for peer in peers:

            try:

                response = requests.post(
                    f"{peer}/append",
                    json=event,
                    timeout=2
                )

                results.append(
                    {
                        "peer": peer,
                        "status": response.json()
                    }
                )

            except Exception as e:

                results.append(
                    {
                        "peer": peer,
                        "error": str(e)
                    }
                )

        return results
