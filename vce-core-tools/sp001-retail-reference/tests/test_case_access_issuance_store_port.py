import ast
from pathlib import Path

import pytest

from test_case_access_issuance_completion import components
from sp001.contracts.case_access_issuance_store import CaseAccessIssuanceStore
from sp001.contracts.case_access_issuance_completion import (
    CaseAccessIssuanceCompletion,
)
from sp001.services.prepared_case_access_completion import (
    PreparedCaseAccessCompleter,
)


class StoreAdapter:
    """Alternative interface adapter backed by real durable SQLite storage."""

    def __init__(self, delegate):
        self.delegate = delegate

    def prepare(self, **kwargs):
        return self.delegate.prepare(**kwargs)

    def prepare_request(self, **kwargs):
        return self.delegate.prepare_request(**kwargs)

    def read_prepared(self, **kwargs):
        return self.delegate.read_prepared(**kwargs)

    def read_completed(self, **kwargs):
        return self.delegate.read_completed(**kwargs)

    def confirm(self, **kwargs):
        return self.delegate.confirm(**kwargs)


def test_completion_accepts_distinct_store_adapter_and_recovers(components):
    _, store, _, _, preparation, signer, protector, _ = components
    adapter = StoreAdapter(store)
    assert isinstance(adapter, CaseAccessIssuanceStore)
    completer = PreparedCaseAccessCompleter(
        store=adapter, signer=signer, protector=protector, clock=lambda: 150,
    )
    token = completer.complete(request_id=preparation.request_id)
    historical = store.read_completed(request_id=preparation.request_id)
    assert isinstance(historical, CaseAccessIssuanceCompletion)
    assert completer.complete(request_id=preparation.request_id) == token
    assert store.read_completed(request_id=preparation.request_id) == historical


def test_incomplete_store_is_rejected(components):
    with pytest.raises(TypeError, match="store"):
        PreparedCaseAccessCompleter(
            store=object(), signer=components[5], protector=components[6],
        )


def test_completion_service_has_no_infrastructure_imports():
    tree = ast.parse(Path(
        "src/sp001/services/prepared_case_access_completion.py"
    ).read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert not (node.module or "").startswith("sp001.infrastructure")
        elif isinstance(node, ast.Import):
            assert not any(
                alias.name.startswith("sp001.infrastructure")
                for alias in node.names
            )


def test_old_imports_preserve_class_identity():
    from sp001.infrastructure.sqlite_case_access_issuance_completions import (
        PreparedCaseAccessCompleter as OldCompleter,
        CaseAccessIssuanceCompletion as OldRecord,
    )
    assert OldCompleter is PreparedCaseAccessCompleter
    assert OldRecord is CaseAccessIssuanceCompletion
