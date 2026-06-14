from collections import defaultdict
from typing import Dict
from typing import Iterable
from typing import List

from epics.ztc10_multi_party_verification.witness_response import (
    WitnessResponse,
)


class StateRootBallotBox:

    @staticmethod
    def group(
        responses: Iterable[WitnessResponse],
    ) -> Dict[str, List[WitnessResponse]]:

        ballot = defaultdict(list)

        for response in responses:
            if response.accepted:
                ballot[
                    response.state_root_hash
                ].append(response)

        return dict(ballot)
