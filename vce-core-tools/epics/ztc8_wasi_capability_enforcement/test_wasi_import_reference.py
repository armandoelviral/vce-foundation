from epics.ztc8_wasi_capability_enforcement.wasi_import_reference import (
    WASIImportReference,
)


def test_wasi_import_reference_contains_module_and_name():

    reference = WASIImportReference(
        module="wasi_snapshot_preview1",
        name="path_open",
    )

    assert reference.module == "wasi_snapshot_preview1"
    assert reference.name == "path_open"


def test_wasi_import_reference_serializes():

    reference = WASIImportReference(
        module="wasi_snapshot_preview1",
        name="path_open",
    )

    assert reference.to_dict() == {
        "module": "wasi_snapshot_preview1",
        "name": "path_open",
    }
