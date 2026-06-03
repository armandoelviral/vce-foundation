class CanonicalLedger:

    def select(
        self,
        ledgers
    ):

        best_peer = None
        best_size = -1

        for peer, ledger in ledgers.items():

            if isinstance(
                ledger,
                dict
            ):
                continue

            size = len(ledger)

            if size > best_size:

                best_size = size
                best_peer = peer

        return {
            "peer": best_peer,
            "ledger_size": best_size
        }
