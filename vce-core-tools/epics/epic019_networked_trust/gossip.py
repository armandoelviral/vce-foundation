class GossipProtocol:

    def __init__(self):

        self.known_messages = {}


    def receive(
        self,
        node_id,
        message
    ):

        if node_id not in self.known_messages:

            self.known_messages[
                node_id
            ] = []


        if message not in self.known_messages[
            node_id
        ]:

            self.known_messages[
                node_id
            ].append(
                message
            )


        return True


    def propagate(
        self,
        peers,
        message
    ):

        for peer in peers:

            self.receive(
                peer,
                message
            )


        return {
            "propagated": True,
            "peers_reached": len(
                peers
            )
        }
