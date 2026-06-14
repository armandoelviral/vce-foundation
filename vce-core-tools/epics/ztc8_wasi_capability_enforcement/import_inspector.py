from epics.ztc8_wasi_capability_enforcement.wasi_capability_mapper import (
    WASICapabilityMapper,
)

from epics.ztc8_wasi_capability_enforcement.wasi_import_reference import (
    WASIImportReference,
)

from epics.ztc8_wasi_capability_enforcement.wasi_policy import (
    WASIPolicy,
)


class ImportInspector:

    @staticmethod
    def inspect(
        reference: WASIImportReference,
    ) -> bool:

        capability = (
            WASICapabilityMapper.map(
                reference
            )
        )

        return WASIPolicy.allow(
            capability
        )
