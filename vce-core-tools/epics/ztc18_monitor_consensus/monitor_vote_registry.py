from typing import List

from epics.ztc18_monitor_consensus.monitor_vote import (
    MonitorVote,
)


class MonitorVoteRegistry:

    def __init__(self):

        self._votes: List[
            MonitorVote
        ] = []

    def add(
        self,
        vote: MonitorVote,
    ) -> None:

        self._votes.append(
            vote
        )

    def all(
        self,
    ) -> List[MonitorVote]:

        return list(
            self._votes
        )

    def count(
        self,
    ) -> int:

        return len(
            self._votes
        )
