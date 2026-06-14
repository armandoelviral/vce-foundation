from epics.ztc8_wasi_capability_enforcement.import_inspector import (
    ImportInspector,
)

from epics.ztc8_wasi_capability_enforcement.wasi_import_reference import (
    WASIImportReference,
)


def test_rejects_filesystem_import():

    reference = WASIImportReference(
        module="wasi_snapshot_preview1",
        name="path_open",
    )

    assert not ImportInspector.inspect(
        reference
    )


def test_rejects_clock_import():

    reference = WASIImportReference(
        module="wasi_snapshot_preview1",
        name="clock_time_get",
    )

    assert not ImportInspector.inspect(
        reference
    )


def test_allows_stdout_import():

    reference = WASIImportReference(
        module="wasi_snapshot_preview1",
        name="fd_write",
    )

    assert ImportInspector.inspect(
        reference
    )
