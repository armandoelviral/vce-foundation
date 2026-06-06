from hypothesis import given
from hypothesis import strategies as st

from epics.epic012_replay_runtime.hash_chain import HashChain


@given(
    st.lists(
        st.text(min_size=1, max_size=50),
        min_size=1,
        max_size=25,
    )
)
def test_hash_chain_produces_hash_for_each_record(records):

    chain = HashChain()

    hashes = [
        chain.append(record)
        for record in records
    ]

    assert len(hashes) == len(records)

    for value in hashes:
        assert isinstance(value, str)
        assert len(value) == 64
