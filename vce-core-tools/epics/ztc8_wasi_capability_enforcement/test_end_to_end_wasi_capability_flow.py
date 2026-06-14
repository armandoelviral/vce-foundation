from epics.ztc8_wasi_capability_enforcement.capability_enforcement_gate import (
    CapabilityEnforcementGate,
)

from epics.ztc8_wasi_capability_enforcement.wasi_import_reference import (
    WASIImportReference,
)


def test_end_to_end_accepts_safe_wasi_imports():

    imports = [
        WASIImportReference(
            module="wasi_snapshot_preview1",
            name="fd_write",
        )
    ]

    assert CapabilityEnforcementGate.admit(
        imports
    )


def test_end_to_end_rejects_unsafe_wasi_imports():

    imports = [
        WASIImportReference(
            module="wasi_snapshot_preview1",
            name="fd_write",
        ),
        WASIImportReference(
            module="wasi_snapshot_preview1",
            name="path_open",
        ),
    ]

    assert not CapabilityEnforcementGate.admit(
        imports
    )

