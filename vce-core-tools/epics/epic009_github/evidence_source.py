from abc import ABC, abstractmethod


class EvidenceSource(ABC):

    @abstractmethod
    def harvest_verifiable_artifacts(self):
        """
        Returns a collection of VCE artifacts.
        """
        raise NotImplementedError
