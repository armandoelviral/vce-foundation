from epics.ztc16_key_rotation_lifecycle.key_validity_window import (
    KeyValidityWindow,
)

from epics.ztc16_key_rotation_lifecycle.key_history_registry import (
    KeyHistoryRegistry,
)

from epics.ztc16_key_rotation_lifecycle.historical_key_resolver import (
    HistoricalKeyResolver,
)


def test_resolves_known_key():

    registry = KeyHistoryRegistry()

    registry.add(
        KeyValidityWindow(
            key_id="key-001",
            start_anchor="anchor-100",
            end_anchor="anchor-200",
        )
    )

    resolver = HistoricalKeyResolver(
        registry
    )

    assert (
        resolver.resolve(
            "anchor-150"
        )
        == "key-001"
    )


def test_returns_none_for_unknown_anchor():

    registry = KeyHistoryRegistry()

    resolver = HistoricalKeyResolver(
        registry
    )

    assert (
        resolver.resolve(
            "anchor-999"
        )
        is None
    )
