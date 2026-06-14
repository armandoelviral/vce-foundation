from epics.ztc16_key_rotation_lifecycle.key_validity_window import (
    KeyValidityWindow,
)

from epics.ztc16_key_rotation_lifecycle.key_history_registry import (
    KeyHistoryRegistry,
)


def test_registry_stores_validity_window():

    registry = KeyHistoryRegistry()

    window = KeyValidityWindow(
        key_id="key-001",
        start_anchor="anchor-100",
        end_anchor="anchor-200",
    )

    registry.add(window)

    assert registry.count() == 1


def test_registry_returns_windows():

    registry = KeyHistoryRegistry()

    window = KeyValidityWindow(
        key_id="key-001",
        start_anchor="anchor-100",
        end_anchor="anchor-200",
    )

    registry.add(window)

    windows = registry.all()

    assert len(windows) == 1
    assert windows[0].key_id == "key-001"


def test_registry_starts_empty():

    registry = KeyHistoryRegistry()

    assert registry.count() == 0
