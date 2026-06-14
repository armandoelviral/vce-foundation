from epics.ztc8_wasi_capability_enforcement.wasi_policy import (
    WASIPolicy,
)


def test_denies_filesystem():

    assert not WASIPolicy.allow(
        "filesystem"
    )


def test_denies_clock():

    assert not WASIPolicy.allow(
        "clock"
    )


def test_denies_random():

    assert not WASIPolicy.allow(
        "random"
    )


def test_allows_stdout():

    assert WASIPolicy.allow(
        "stdout"
    )


def test_denies_unknown():

    assert not WASIPolicy.allow(
        "unknown"
    )
