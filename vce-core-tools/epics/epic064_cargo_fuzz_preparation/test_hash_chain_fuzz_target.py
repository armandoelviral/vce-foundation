from hypothesis import given
from hypothesis import strategies as st

from epics.epic012_replay_runtime.hash_chain import HashChain


@given(
    st.lists(
        st.text(),
        min_size=0,
        max_size=100,
    )
)
def test_hash_chain_never_crashes(records):

    chain = HashChain()

    for record in records:
        value = chain.append(record)

        assert value is not None
