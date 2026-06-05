from epics.epic030_log_correctness.commit_index import (
    CommitIndex
)

index = CommitIndex()

print(
    index.advance(
        1
    )
)

print(
    index.advance(
        3
    )
)

print(
    index.advance(
        2
    )
)

print(
    index.value
)
