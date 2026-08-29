from dataclasses import dataclass
from pathlib import Path
import re


KNOWLEDGE_INGESTION_REGISTRY_FILE_SUFFIX = ".registry.json"
MAXIMUM_STORAGE_LOGICAL_NAME_LENGTH = 128


@dataclass(frozen=True, slots=True)
class KnowledgeIngestionRegistryStorageLocation:
    """Safe deterministic location identity without filesystem mutation."""

    storage_root: Path
    logical_name: str

    def __post_init__(self) -> None:
        if not isinstance(
            self.storage_root,
            Path,
        ):
            raise TypeError(
                "storage_root must be a Path"
            )

        if not self.storage_root.is_absolute():
            raise ValueError(
                "storage_root must be absolute"
            )

        if (
            self.storage_root.parent
            == self.storage_root
        ):
            raise ValueError(
                "storage_root must not be a filesystem root"
            )

        if not isinstance(
            self.logical_name,
            str,
        ):
            raise TypeError(
                "logical_name must be a string"
            )

        if not self.logical_name:
            raise ValueError(
                "logical_name must not be empty"
            )

        if len(
            self.logical_name
        ) > MAXIMUM_STORAGE_LOGICAL_NAME_LENGTH:
            raise ValueError(
                "logical_name must contain at most "
                "128 characters"
            )

        if self.logical_name in (
            ".",
            "..",
        ):
            raise ValueError(
                "logical_name must not be a reserved path component"
            )

        if re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9._-]*",
            self.logical_name,
        ) is None:
            raise ValueError(
                "logical_name must contain only ASCII letters, "
                "digits, dots, underscores or hyphens and must "
                "start with an alphanumeric character"
            )

        candidate = self.artifact_path

        if candidate.parent != self.storage_root:
            raise ValueError(
                "artifact path must remain inside storage_root"
            )

    @property
    def artifact_path(self) -> Path:
        """Resolve the fixed artifact filename without touching storage."""

        return self.storage_root / (
            self.logical_name
            + KNOWLEDGE_INGESTION_REGISTRY_FILE_SUFFIX
        )
