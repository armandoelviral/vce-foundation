from github_connector import GitHubActionsConnector
import os

token = os.environ["GITHUB_TOKEN"]

connector = GitHubActionsConnector(
    token=token,
    owner="armandoelviral",
    repo="vce-foundation"
)

data = connector.harvest_verifiable_artifacts()

print(data.keys())

if "workflow_runs" in data:
    print(
        f"Workflow runs found: "
        f"{len(data['workflow_runs'])}"
    )
