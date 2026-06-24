def calculate_constitutional_trust_score(
    reputation_score: int,
    credibility_score: int,
    trust_score: int,
):
    return int(
        (
            reputation_score
            + credibility_score
            + trust_score
        )
        / 3
    )
