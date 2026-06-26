def decision_is_final(outcome: str):
    return outcome in {
        "accepted",
        "rejected",
    }
