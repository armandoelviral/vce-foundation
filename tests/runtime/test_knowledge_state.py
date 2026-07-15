from has.runtime.knowledge_state import KnowledgeState


def test_contains_observation():

    assert (
        KnowledgeState.OBSERVATION.value
        == "observation"
    )


def test_contains_principle():

    assert (
        KnowledgeState.PRINCIPLE.value
        == "principle"
    )
