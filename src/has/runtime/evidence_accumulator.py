from dataclasses import replace

from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)


class EvidenceAccumulator:

    def record(
        self,
        artifact: KnowledgeArtifact,
        amount: int = 1,
    ) -> KnowledgeArtifact:

        if amount < 1:
            raise ValueError(
                "amount must be greater than zero"
            )

        return replace(
            artifact,
            evidence_count=(
                artifact.evidence_count + amount
            ),
        )
