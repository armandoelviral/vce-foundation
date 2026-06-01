class PeerDiscovery:

    def __init__(self):

        self.peers = {}


    def register(
        self,
        node_id,
        endpoint
    ):

        self.peers[
            node_id
        ] = {
            "endpoint": endpoint,
            "active": True
        }


        return True


    def remove(
        self,
        node_id
    ):

        if node_id in self.peers:

            self.peers[
                node_id
            ][
                "active"
            ] = False


    def active_peers(
        self
    ):

        return {
            node: data

            for node, data
            in self.peers.items()

            if data[
                "active"
            ]
        }
