from github_connector import GitHubActionsConnector


def test_connector_stores_configuration():

    connector = GitHubActionsConnector(
        token="test-token",
        owner="armandoelvira1",
        repo="vce-foundation",
    )

    assert connector.token == "test-token"
    assert connector.owner == "armandoelvira1"
    assert connector.repo == "vce-foundation"
