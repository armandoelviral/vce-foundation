from has.runtime.knowledge_artifact import KnowledgeArtifact


class KnowledgeTransitionPolicy:

    def can_promote(
        self,
        artifact: KnowledgeArtifact,
    ) -> bool:

        raise NotImplementedError
