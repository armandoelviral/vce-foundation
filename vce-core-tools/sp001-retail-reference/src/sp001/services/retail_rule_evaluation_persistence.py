from collections.abc import Callable

from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportIdentity,
    RetailRuleEvaluationReportStore,
    StoredRetailRuleEvaluationReport,
)
from sp001.services.retail_rule_evaluation_report import (
    RetailRuleEvaluationReport,
)


class RetailRuleEvaluationPersistence:
    """Validate report documents around an injected append-only store."""

    def __init__(
        self,
        *,
        store: RetailRuleEvaluationReportStore,
        serialize: Callable[[RetailRuleEvaluationReport], str],
        deserialize: Callable[[str], RetailRuleEvaluationReport],
    ) -> None:
        if not isinstance(store, RetailRuleEvaluationReportStore):
            raise TypeError("store must implement the report store port")
        if not callable(serialize) or not callable(deserialize):
            raise TypeError("serialize and deserialize must be callable")
        self._store = store
        self._serialize = serialize
        self._deserialize = deserialize

    def _decode(self, document: str) -> RetailRuleEvaluationReport:
        report = self._deserialize(document)
        if type(report) is not RetailRuleEvaluationReport:
            raise TypeError("deserializer returned an invalid report")
        return report

    def save(
        self,
        *,
        identity: RetailRuleEvaluationReportIdentity,
        report: RetailRuleEvaluationReport,
    ) -> RetailRuleEvaluationReport:
        if not isinstance(identity, RetailRuleEvaluationReportIdentity):
            raise TypeError("identity must be a report identity")
        if type(report) is not RetailRuleEvaluationReport:
            raise TypeError("report must be a RetailRuleEvaluationReport")

        document = self._serialize(report)
        candidate = StoredRetailRuleEvaluationReport(identity, document)
        validated = self._decode(document)
        if validated != report:
            raise ValueError("serialized document changes report content")

        confirmed = self._store.put(report=candidate)
        if not isinstance(confirmed, StoredRetailRuleEvaluationReport):
            raise TypeError("store returned an invalid confirmation")
        if confirmed != candidate:
            raise ValueError("store confirmation differs from submitted report")
        return validated

    def recover(
        self, *, identity: RetailRuleEvaluationReportIdentity
    ) -> RetailRuleEvaluationReport | None:
        if not isinstance(identity, RetailRuleEvaluationReportIdentity):
            raise TypeError("identity must be a report identity")
        stored = self._store.get(identity=identity)
        if stored is None:
            return None
        if not isinstance(stored, StoredRetailRuleEvaluationReport):
            raise TypeError("store returned an invalid stored report")
        if stored.identity != identity:
            raise ValueError("store returned a different report identity")
        return self._decode(stored.document)
