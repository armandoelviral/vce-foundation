from epics.ztc8_wasi_capability_enforcement.wasi_import_reference import (
    WASIImportReference,
)


class WASICapabilityMapper:

    MAP = {
        "path_open": "filesystem",
        "fd_read": "filesystem",
        "fd_write": "stdout",
        "clock_time_get": "clock",
        "random_get": "random",
        "sock_open": "network",
    }

    @classmethod
    def map(
        cls,
        reference: WASIImportReference,
    ) -> str:

        return cls.MAP.get(
            reference.name,
            "unknown",
        )
