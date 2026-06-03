from epics.epic027_catchup.canonical_pull import (
    CanonicalPull
)

pull = CanonicalPull()

result = pull.pull(
    "http://127.0.0.1:8000"
)

print(
    result["peer"]
)

print(
    len(
        result["ledger"]
    )
)

print(
    result["ledger"]
)
