from typing import Iterable

from epics.ztc8_wasi_capability_enforcement.import_inspector import (
    ImportInspector,
)

from epics.ztc8_wasi_capability_enforcement.wasi_import_reference import (
    WASIImportReference,
)


class CapabilityEnforcementGate:

    @staticmethod
    def admit(
        imports: Iterable[WASIImportReference],
    ) -> bool:

        return all(
            ImportInspector.inspect(
                reference
            )
            for reference in imports
        )
