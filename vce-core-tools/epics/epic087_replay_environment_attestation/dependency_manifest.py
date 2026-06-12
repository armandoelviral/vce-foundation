from dataclasses import dataclass


@dataclass(frozen=True)
class DependencyManifest:
    manifest_id: str
    dependencies: dict

    def to_dict(self):

        return {
            "manifest_id": self.manifest_id,
            "dependencies": self.dependencies,
        }

    def dependency_count(self):

        return len(
            self.dependencies
        )

    def get_version(
        self,
        dependency_name,
    ):

        return self.dependencies.get(
            dependency_name
        )
