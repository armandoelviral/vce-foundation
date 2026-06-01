import random

from epics.epic016_production_verification.invariant_suite import (
    InvariantSuite
)


class PropertyTesting:

    def __init__(self):

        self.suite = InvariantSuite()


    def random_state(self):

        return {
            "execution": random.choice(
                [
                    "VERIFIED",
                    "FAILED"
                ]
            ),

            "trust": random.choice(
                [
                    "ACCEPTED",
                    "REJECTED"
                ]
            ),

            "ledger": random.choice(
                [
                    "COMMITTED",
                    "CORRUPTED"
                ]
            ),

            "tamper_evident": random.choice(
                [
                    True,
                    False
                ]
            )
        }


    def run(self, iterations=10000):

        violations = 0

        for _ in range(iterations):

            state = self.random_state()

            result = (
                self.suite.verify_release_state(
                    state
                )
            )

            if result["passed"]:

                expected = (
                    state["execution"] == "VERIFIED"
                    and state["trust"] == "ACCEPTED"
                    and state["ledger"] == "COMMITTED"
                    and state["tamper_evident"] is True
                )

                if not expected:
                    violations += 1


        return {
            "iterations": iterations,
            "violations": violations,
            "passed": violations == 0
        }
