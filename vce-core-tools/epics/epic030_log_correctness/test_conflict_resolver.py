from epics.epic030_log_correctness.conflict_resolver import (
    ConflictResolver
)


resolver = ConflictResolver()


canonical_log = [
    {
        "sequence": 1
    },
    {
        "sequence": 2
    },
    {
        "sequence": 3
    },
    {
        "sequence": 4
    },
    {
        "sequence": 5
    }
]


divergent_log = [
    {
        "sequence": 1
    },
    {
        "sequence": 2
    },
    {
        "sequence": 3
    },
    {
        "sequence": 4
    },
    {
        "sequence": 5
    }
]

result = resolver.resolve(
    canonical_log,
    divergent_log
)


print(result)
