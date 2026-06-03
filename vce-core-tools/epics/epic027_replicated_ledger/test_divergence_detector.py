from epics.epic027_replicated_ledger.divergence_detector import (
    DivergenceDetector
)

detector = DivergenceDetector()

result = detector.evaluate(
    {
        "replicated": False,
        "nodes": 3,
        "unique_ledgers": 2
    }
)

print(result)
