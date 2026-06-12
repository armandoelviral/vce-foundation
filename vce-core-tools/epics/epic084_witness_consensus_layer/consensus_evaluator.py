def evaluate_consensus(
    collection,
    policy,
):

    observed_count = collection.observed_count()

    achieved = policy.is_satisfied(
        observed_count
    )

    return {
        "consensus": (
            "CONSENSUS_ACHIEVED"
            if achieved
            else "CONSENSUS_NOT_ACHIEVED"
        ),
        "policy": policy.policy_label(),
        "observed_votes": observed_count,
        "total_votes": collection.total_count(),
    }
