from dataclasses import fields, FrozenInstanceError
from dataclasses import replace

import pytest

from sp001.contracts.product001_documentary_inputs import (
    Product001DocumentaryInputs,
)

from test_knowledge_source_retrieval import (
    CONTENT,
    create_status,
    create_context,
    create_binding,
)

from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeSourceEffectivePeriod,
)
from sp001.contracts.knowledge_source_supersession import (
    KnowledgeSourceSupersessionGraph,
)

from datetime import datetime, timezone


def make_inputs():
    source = create_status()

    return Product001DocumentaryInputs(
        source_status=source,
        content=CONTENT,
        effective_period=KnowledgeSourceEffectivePeriod(
            source_status=source,
            effective_from=datetime(
                2026, 3, 1, tzinfo=timezone.utc
            ),
        ),
        retrieval_context=create_context(),
        authority_bindings=(create_binding(source),),
        supersession_graph=KnowledgeSourceSupersessionGraph(
            supersessions=()
        ),
    )


def test_documentary_inputs_have_exact_fields():
    names = {field.name for field in fields(
        Product001DocumentaryInputs
    )}

    assert names == {
        "source_status",
        "content",
        "effective_period",
        "retrieval_context",
        "authority_bindings",
        "supersession_graph",
    }


def test_documentary_inputs_are_immutable():
    value = make_inputs()

    with pytest.raises(FrozenInstanceError):
        value.content = b"tampered"


def test_documentary_inputs_reject_decision_injection():
    value = make_inputs()

    with pytest.raises(TypeError):
        Product001DocumentaryInputs(
            **{
                field.name: getattr(value, field.name)
                for field in fields(value)
            },
            retrieval_decision=object(),
        )


def test_documentary_inputs_reject_invalid_content_type():
    value = make_inputs()

    with pytest.raises(TypeError):
        replace(value, content="not bytes")


def test_documentary_inputs_reject_invalid_binding_type():
    value = make_inputs()

    with pytest.raises(TypeError):
        replace(value, authority_bindings=(object(),))
