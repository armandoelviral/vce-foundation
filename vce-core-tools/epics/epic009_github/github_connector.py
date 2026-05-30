import requests

from evidence_source import EvidenceSource


class GitHubActionsConnector(EvidenceSource):

    def __init__(self, token: str, owner: str, repo: str):
        self.token = token
        self.owner = owner
        self.repo = repo

    def harvest_verifiable_artifacts(self):

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

        url = (
            f"https://api.github.com/repos/"
            f"{self.owner}/{self.repo}/actions/runs"
        )

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()
