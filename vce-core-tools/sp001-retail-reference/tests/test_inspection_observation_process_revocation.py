import multiprocessing
from queue import Empty

import pytest

import test_sqlite_authorized_inspection_observations as setup
from test_inspection_observation_revocation_ordering import instrument, revoke


def worker(path, operation, definition, results, began, held, release):
    """Each child creates its own backend and SQLite connections."""
    try:
        principal = definition.principal
        with pytest.MonkeyPatch.context() as patch:
            if operation == "revoke":
                owner = setup.SqliteCaseAccessGrants(database_path=path)
            else:
                owner = setup.Backend(
                    database_path=path,
                    expected_audience="OBS",
                    clock=lambda: 150,
                )

            events = {}
            if began is not None:
                events["began"] = began
            if held is not None:
                events.update(before_commit=held, release=release)
            instrument(patch, owner, **events)

            if operation == "revoke":
                assert revoke(owner, principal, definition) is True
            else:
                owner.save_authorized(
                    access=setup.access(principal, setup.SAVE),
                    observation=setup.observation(),
                )
        results.put((operation, "ok"))
    except setup.Denied:
        results.put((operation, "denied"))
    except BaseException as error:
        results.put((operation, "error", type(error).__name__, str(error)))


@pytest.mark.parametrize("first", ["revoke", "save"])
def test_process_commit_order_controls_save_and_retry(tmp_path, first):
    path, _, _, principal, grants = setup.environment(tmp_path)
    definition = setup.grant(grants, principal, setup.SAVE)
    item = setup.observation()

    context = multiprocessing.get_context("spawn")
    results = context.Queue()
    held = context.Event()
    release = context.Event()
    follower_began = context.Event()
    second = "save" if first == "revoke" else "revoke"

    leader = context.Process(
        target=worker,
        args=(path, first, definition, results, None, held, release),
    )
    follower = context.Process(
        target=worker,
        args=(
            path, second, definition, results,
            follower_began, None, release,
        ),
    )
    started = []
    try:
        leader.start()
        started.append(leader)
        assert held.wait(10), "first process did not reach COMMIT"

        follower.start()
        started.append(follower)
        assert follower_began.wait(10), "second process did not attempt BEGIN"

        # The leader holds the write transaction until this explicit barrier.
        release.set()

        for process in started:
            process.join(15)
            assert not process.is_alive(), "child did not terminate"
            assert process.exitcode == 0

        received = []
        for _ in range(2):
            try:
                received.append(results.get(timeout=5))
            except Empty:
                pytest.fail("child result missing")

        expected_save = "denied" if first == "revoke" else "ok"
        assert sorted(received) == sorted([
            ("revoke", "ok"),
            ("save", expected_save),
        ])
    finally:
        release.set()
        for process in started:
            process.join(2)
            if process.is_alive():
                process.terminate()
                process.join(5)
        results.close()
        results.join_thread()

    # Verify durable effects using newly opened connections.
    reopened = setup.SqliteRetailInspectionObservationStore(database_path=path)
    stored = reopened.get(identity=setup.key(item))
    if first == "revoke":
        assert stored is None
        assert setup.count(path) == 0
    else:
        assert stored is not None
        assert stored.document == setup.serialize(item)
        assert setup.count(path) == 1

    fresh_grants = setup.SqliteCaseAccessGrants(database_path=path)
    assert fresh_grants.permits(
        principal=principal,
        permission=definition.permission,
        at_time=150,
    ) is False

    fresh_backend = setup.Backend(
        database_path=path,
        expected_audience="OBS",
        clock=lambda: 150,
    )
    with pytest.raises(setup.Denied):
        fresh_backend.save_authorized(
            access=setup.access(principal, setup.SAVE),
            observation=item,
        )

    expected_count = 0 if first == "revoke" else 1
    assert setup.count(path) == expected_count
    assert reopened.get(identity=setup.key(item)) == stored
