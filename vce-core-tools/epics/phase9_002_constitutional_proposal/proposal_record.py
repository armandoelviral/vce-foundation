from dataclasses import dataclass


@dataclass(frozen=True)
class ProposalRecord:
    proposal_id: str
    intent_id: str
    title: str

    def __post_init__(self):
        if not self.proposal_id:
            raise ValueError("proposal_id is required")

        if not self.intent_id:
            raise ValueError("intent_id is required")

        if not self.title:
            raise ValueError("title is required")
