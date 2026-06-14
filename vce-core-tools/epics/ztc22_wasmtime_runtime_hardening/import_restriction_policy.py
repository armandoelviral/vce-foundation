class ImportRestrictionPolicy:

    def __init__(
        self,
        allowed_imports,
    ):

        self.allowed_imports = (
            allowed_imports
        )

    def allow(
        self,
        import_name: str,
    ) -> bool:

        return (
            import_name
            in self.allowed_imports
        )
