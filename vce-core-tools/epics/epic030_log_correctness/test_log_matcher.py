from epics.epic030_log_correctness.log_matcher import (
    LogMatcher
)

matcher = LogMatcher()

result = matcher.compare(
    [
        {"sequence":1},
        {"sequence":2},
        {"sequence":3}
    ],
    [
        {"sequence":1},
        {"sequence":2},
        {"sequence":3}
    ]
)

print(result)
