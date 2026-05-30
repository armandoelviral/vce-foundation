from evidence_source import EvidenceSource


class GitHubActionsConnector(EvidenceSource):

    def __init__(self, token: str):
        self.token = token

    def harvest_verifiable_artifacts(self):
        raise NotImplementedError(
            "Epic 009 implementation pending"
        )
