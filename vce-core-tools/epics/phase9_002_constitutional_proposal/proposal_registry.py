from epics.phase9_002_constitutional_proposal.proposal_record import (
    ProposalRecord,
)


class ProposalRegistry:
    def __init__(self):
        self._records = []

    def add(self, proposal: ProposalRecord):
        self._records.append(proposal)

    def records(self):
        return list(self._records)
