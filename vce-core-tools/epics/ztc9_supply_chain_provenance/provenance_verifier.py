from epics.ztc9_supply_chain_provenance.provenance_chain import (
    ProvenanceChain,
)


class ProvenanceVerifier:

    @staticmethod
    def verify(
        chain: ProvenanceChain,
    ) -> bool:

        if (
            chain.source.commit_sha
            != chain.build.source_commit
        ):
            return False

        if (
            chain.build.build_id
            != chain.artifact.build_id
        ):
            return False

        return True
