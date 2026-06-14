from typing import List

from epics.ztc14_transparency_gossip_protocol.gossip_message import (
    GossipMessage,
)


class GossipRegistry:

    def __init__(self):

        self._messages: List[
            GossipMessage
        ] = []

    def add(
        self,
        message: GossipMessage,
    ) -> None:

        self._messages.append(
            message
        )

    def all(
        self,
    ) -> List[GossipMessage]:

        return list(
            self._messages
        )

    def count(
        self,
    ) -> int:

        return len(
            self._messages
        )
