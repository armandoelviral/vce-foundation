class EvidenceSchemaValidator:

    REQUIRED_FIELDS = {
        "artifact_id",
        "schema_version",
        "state_root_hash",
    }

    @classmethod
    def validate(
        cls,
        evidence: dict,
    ) -> bool:

        return cls.REQUIRED_FIELDS.issubset(
            evidence.keys()
        )
