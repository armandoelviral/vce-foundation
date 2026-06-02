class MembershipView:

    def __init__(self):

        self.members = {}

    def update(
        self,
        discovered
    ):

        for peer in discovered:

            node_id = peer.get(
                "node_id",
                peer["peer"]
            )

            self.members[node_id] = {
                "peer": peer["peer"],
                "alive": peer["alive"]
            }

    def alive_nodes(self):

        return [
            node_id
            for node_id, data
            in self.members.items()
            if data["alive"]
        ]

    def dead_nodes(self):

        return [
            node_id
            for node_id, data
            in self.members.items()
            if not data["alive"]
        ]
