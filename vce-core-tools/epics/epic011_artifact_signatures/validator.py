from abc import ABC, abstractmethod


class ArtifactValidator(ABC):

    @abstractmethod
    def validate(self, artifact: dict) -> bool:
        pass
