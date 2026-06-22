from phase4.constitutional_evolution_layer.ratification_vote import (
    RatificationVote,
)


def test_contains_amendment():

    vote = RatificationVote(
        amendment_id="amendment-001",
        approved=True,
    )

    assert (
        vote.amendment_id
        == "amendment-001"
    )


def test_contains_approval():

    vote = RatificationVote(
        amendment_id="amendment-001",
        approved=True,
    )

    assert vote.approved is True


def test_serializes():

    vote = RatificationVote(
        amendment_id="amendment-001",
        approved=True,
    )

    assert vote.to_dict() == {
        "amendment_id":
            "amendment-001",
        "approved":
            True,
    }
