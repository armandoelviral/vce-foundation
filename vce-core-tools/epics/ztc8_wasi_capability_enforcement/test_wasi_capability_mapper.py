from epics.ztc8_wasi_capability_enforcement.wasi_capability_mapper import (
    WASICapabilityMapper,
)

from epics.ztc8_wasi_capability_enforcement.wasi_import_reference import (
    WASIImportReference,
)


def test_maps_path_open_to_filesystem():

    reference = WASIImportReference(
        module="wasi_snapshot_preview1",
        name="path_open",
    )

    assert WASICapabilityMapper.map(reference) == "filesystem"


def test_maps_clock_time_get_to_clock():

    reference = WASIImportReference(
        module="wasi_snapshot_preview1",
        name="clock_time_get",
    )

    assert WASICapabilityMapper.map(reference) == "clock"


def test_maps_random_get_to_random():

    reference = WASIImportReference(
        module="wasi_snapshot_preview1",
        name="random_get",
    )

    assert WASICapabilityMapper.map(reference) == "random"


def test_maps_unknown_import_to_unknown():

    reference = WASIImportReference(
        module="custom",
        name="unknown",
    )

    assert WASICapabilityMapper.map(reference) == "unknown"
