from abc import ABC
from abc import abstractmethod

from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)


class KnowledgeTransition(ABC):

    @abstractmethod
    def execute(
        self,
        artifact: KnowledgeArtifact,
    ) -> KnowledgeArtifact:
        ...
