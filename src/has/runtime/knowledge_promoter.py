from dataclasses import replace

from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)


class KnowledgePromoter:

    def promote(
        self,
        artifact: KnowledgeArtifact,
        target_state: KnowledgeState,
    ) -> KnowledgeArtifact:

        return replace(
            artifact,
            state=target_state,
        )
