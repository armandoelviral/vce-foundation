class InvariantSuite:

    def verify_release_state(
        self,
        state
    ):

        invariants = {
            "execution_verified":
                state.get("execution")
                == "VERIFIED",

            "trust_accepted":
                state.get("trust")
                == "ACCEPTED",

            "ledger_committed":
                state.get("ledger")
                == "COMMITTED",

            "tamper_evidence_active":
                state.get(
                    "tamper_evident"
                )
                is True
        }


        return {
            "passed": all(
                invariants.values()
            ),
            "checks": invariants
        }
