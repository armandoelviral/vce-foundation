from __future__ import annotations


class EvidenceCollector:
    """
    Aggregate Runtime execution evidence.
    """

    def collect(
        self,
        execution_results: tuple[tuple[str, str], ...],
    ) -> tuple[tuple[str, ...], str]:

        evidence = tuple(
            result[0]
            for result in execution_results
        )

        decision = (
            "PASS"
            if all(
                result[1] == "PASS"
                for result in execution_results
            )
            else "FAIL"
        )

        return (
            evidence,
            decision,
        )
