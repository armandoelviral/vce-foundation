from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SourceProvenanceRecord:
    repository_url: str
    commit_sha: str
    branch: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "repository_url": self.repository_url,
            "commit_sha": self.commit_sha,
            "branch": self.branch,
        }
