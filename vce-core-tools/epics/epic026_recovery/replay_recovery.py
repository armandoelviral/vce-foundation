class ReplayRecovery:

    def rebuild(
        self,
        ledger
    ):

        state = {
            "bootstrapped": False,
            "attestations": 0
        }

        for entry in ledger:

            event = entry["event"]

            if event == "BOOTSTRAP":

                state["bootstrapped"] = True

            elif event == "ATTESTATION":

                state["attestations"] += 1

        return state
