from sp001.contracts.retail_inspection_observation import (
    RetailInspectionObservation,
)
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationIdentity,
    RetailInspectionObservationStore,
    StoredRetailInspectionObservation,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
    deserialize_retail_inspection_observation as deserialize,
)


class RetailInspectionObservationPersistence:
    """Validate canonical observations around an injected append-only store.

    No authentication, authorization, succession policy or verdict is added.
    A failed save may have committed; recover by exact identity before retrying.
    """

    def __init__(self, *, store: RetailInspectionObservationStore) -> None:
        if not isinstance(store, RetailInspectionObservationStore):
            raise TypeError("store must implement the observation store port")
        self._store = store

    def _decode(self, stored, expected_identity):
        if type(stored) is not StoredRetailInspectionObservation:
            raise TypeError("store returned an invalid stored observation")
        if stored.identity != expected_identity:
            raise ValueError("store returned a different observation identity")
        observation = deserialize(stored.document)
        if (
            observation.observation_id != expected_identity.observation_id
            or observation.observation_version
            != expected_identity.observation_version
        ):
            raise ValueError("document identity/version differs from storage key")
        return observation

    def save(
        self, *, observation: RetailInspectionObservation,
    ) -> RetailInspectionObservation:
        if type(observation) is not RetailInspectionObservation:
            raise TypeError("observation must be a RetailInspectionObservation")
        identity = RetailInspectionObservationIdentity(
            observation.observation_id, observation.observation_version,
        )
        candidate = StoredRetailInspectionObservation(
            identity, serialize(observation),
        )
        validated = self._decode(candidate, identity)
        if validated != observation:
            raise ValueError("serialized document changes observation content")

        confirmed = self._store.put(observation=candidate)
        recovered = self._decode(confirmed, identity)
        if confirmed != candidate or recovered != validated:
            raise ValueError("store confirmation differs from submitted observation")
        return recovered

    def recover(
        self, *, identity: RetailInspectionObservationIdentity,
    ) -> RetailInspectionObservation | None:
        if type(identity) is not RetailInspectionObservationIdentity:
            raise TypeError("identity must be an observation identity")
        stored = self._store.get(identity=identity)
        if stored is None:
            return None
        return self._decode(stored, identity)
