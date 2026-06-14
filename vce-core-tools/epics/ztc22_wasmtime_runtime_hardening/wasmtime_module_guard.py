class WasmtimeModuleGuard:

    @staticmethod
    def allow(
        module_name: str,
        module_hash: str,
    ) -> bool:

        if not module_name:
            return False

        if not module_hash:
            return False

        return True
