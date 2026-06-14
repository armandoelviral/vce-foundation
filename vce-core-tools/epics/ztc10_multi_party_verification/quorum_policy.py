class QuorumPolicy:

    @staticmethod
    def select(
        ballot: dict,
        minimum_witnesses: int,
    ):

        for state_root, witnesses in ballot.items():

            if (
                len(witnesses)
                >= minimum_witnesses
            ):
                return state_root

        return None
