import requests


class PeerTransport:

    def attest_peer(
        self,
        peer_url,
        artifact
    ):

        response = requests.post(
            f"{peer_url}/attest",
            json={
                "artifact": artifact
            },
            timeout=5
        )

        return response.json()


    def attest_many(
        self,
        peers,
        artifact
    ):

        results = []

        for peer in peers:

            try:

                result = self.attest_peer(
                    peer,
                    artifact
                )

                results.append(
                    result
                )

            except Exception as exc:

                results.append(
                    {
                        "peer": peer,
                        "error": str(exc)
                    }
                )

        return results
