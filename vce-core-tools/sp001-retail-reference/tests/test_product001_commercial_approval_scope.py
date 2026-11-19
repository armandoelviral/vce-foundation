from dataclasses import replace

import pytest

from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeScopeMode,
    KnowledgeScopeSelection,
    KnowledgeSourceScope,
)
from sp001.services.product001_commercial_approval_scope import (
    commercial_scope_covers,
    selection_covers,
)


def all_selection():
    return KnowledgeScopeSelection(KnowledgeScopeMode.ALL, ())


def explicit(*ids):
    return KnowledgeScopeSelection(KnowledgeScopeMode.EXPLICIT, ids)


@pytest.mark.parametrize(
    "grant,requested,expected",
    [
        (all_selection(), all_selection(), True),
        (all_selection(), explicit("a"), True),
        (explicit("a", "b"), explicit("a"), True),
        (explicit("a"), explicit("a", "b"), False),
        (explicit("a"), all_selection(), False),
        (explicit("a"), explicit("b"), False),
    ],
)
def test_selection_coverage(grant, requested, expected):
    assert selection_covers(grant, requested) is expected


def scope():
    return KnowledgeSourceScope(
        organization_id="org-001",
        customer_id="customer-001",
        jurisdiction="MX",
        commercial_channel_id="retail",
        document_type=KnowledgeDocumentType.PLANOGRAM,
        point_of_sale_scope=explicit("pos-001", "pos-002"),
        department_scope=explicit("baby", "clothing"),
        campaign_id="campaign-001",
    )


def test_matching_scope():
    assert commercial_scope_covers(scope(), scope())


@pytest.mark.parametrize(
    "field,value",
    [
        ("organization_id", "other"),
        ("customer_id", "other"),
        ("jurisdiction", "US"),
        ("commercial_channel_id", "wholesale"),
        ("document_type", KnowledgeDocumentType.LOOKBOOK),
        ("campaign_id", "other"),
    ],
)
def test_scope_identity_mismatch(field, value):
    assert not commercial_scope_covers(
        scope(),
        replace(scope(), **{field: value}),
    )


def test_point_of_sale_subset():
    requested = replace(
        scope(),
        point_of_sale_scope=explicit("pos-001"),
    )
    assert commercial_scope_covers(scope(), requested)


def test_department_subset():
    requested = replace(
        scope(),
        department_scope=explicit("baby"),
    )
    assert commercial_scope_covers(scope(), requested)


def test_point_of_sale_expansion_rejected():
    requested = replace(
        scope(),
        point_of_sale_scope=explicit("pos-001", "pos-003"),
    )
    assert not commercial_scope_covers(scope(), requested)


def test_department_expansion_rejected():
    requested = replace(
        scope(),
        department_scope=all_selection(),
    )
    assert not commercial_scope_covers(scope(), requested)


def test_unrestricted_campaign_grant():
    grant = replace(scope(), campaign_id=None)
    assert commercial_scope_covers(grant, scope())


@pytest.mark.parametrize(
    "grant,requested",
    [
        (None, all_selection()),
        (all_selection(), None),
    ],
)
def test_invalid_selection_types(grant, requested):
    with pytest.raises(TypeError):
        selection_covers(grant, requested)


@pytest.mark.parametrize(
    "grant,requested",
    [
        (None, scope()),
        (scope(), None),
    ],
)
def test_invalid_scope_types(grant, requested):
    with pytest.raises(TypeError):
        commercial_scope_covers(grant, requested)
