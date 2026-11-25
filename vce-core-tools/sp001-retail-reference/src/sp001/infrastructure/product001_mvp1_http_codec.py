"""Strict laboratory HTTP decoding for PRODUCT-001 MVP1.

No authentication, authorization, persistence, or network effects.
"""

import base64
import binascii
from collections.abc import Mapping
from dataclasses import fields

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.product001_mvp1_commitment_certificate import (
    CommitmentCertificateV1,
    CommitmentContextV1,
)
from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeScopeMode,
    KnowledgeScopeSelection,
    KnowledgeSourceScope,
)
from sp001.contracts.product001_document_version_binding import (
    Product001DocumentVersionBinding,
)
from sp001.contracts.product001_commercial_approval_decision import (
    Product001CommercialApprovalDecision,
    Product001CommercialDecision,
)
from sp001.services.product001_mvp1_execution_gate import (
    MVP1Authorization,
)


def _object(value, expected):
    if not isinstance(value, dict):
        raise TypeError("JSON object required")
    if set(value) != set(expected):
        raise ValueError("invalid object fields")
    return value


def _fields(cls):
    return tuple(field.name for field in fields(cls))


def _string(value):
    if not isinstance(value, str):
        raise TypeError("string required")
    return value


def _integer(value):
    if type(value) is not int:
        raise TypeError("integer required")
    return value


def _enum(cls, value):
    if not isinstance(value, str):
        raise TypeError("enum string required")
    return cls(value)


def _selection(value):
    value = _object(value, _fields(KnowledgeScopeSelection))
    ids = value["ids"]
    if type(ids) is not list:
        raise TypeError("scope ids must be a JSON array")
    return KnowledgeScopeSelection(
        mode=_enum(KnowledgeScopeMode, value["mode"]),
        ids=tuple(_string(item) for item in ids),
    )


def _identity(value):
    value = _object(value, _fields(KnowledgeSourceIdentity))
    digest = _object(
        value["source_content_digest"],
        _fields(KnowledgeContentDigest),
    )
    return KnowledgeSourceIdentity(
        source_id=_string(value["source_id"]),
        source_version=_string(value["source_version"]),
        source_content_digest=KnowledgeContentDigest(
            algorithm=_string(digest["algorithm"]),
            value=_string(digest["value"]),
        ),
    )


def _scope(value):
    value = _object(value, _fields(KnowledgeSourceScope))
    campaign = value["campaign_id"]
    if campaign is not None:
        campaign = _string(campaign)
    return KnowledgeSourceScope(
        organization_id=_string(value["organization_id"]),
        customer_id=_string(value["customer_id"]),
        jurisdiction=_string(value["jurisdiction"]),
        commercial_channel_id=_string(value["commercial_channel_id"]),
        document_type=_enum(
            KnowledgeDocumentType,
            value["document_type"],
        ),
        point_of_sale_scope=_selection(
            value["point_of_sale_scope"]
        ),
        department_scope=_selection(
            value["department_scope"]
        ),
        campaign_id=campaign,
    )


def _binding(value):
    value = _object(
        value,
        _fields(Product001DocumentVersionBinding),
    )
    return Product001DocumentVersionBinding(
        source_id=_string(value["source_id"]),
        commercial_version=_integer(
            value["commercial_version"]
        ),
        document_version=_string(value["document_version"]),
        point_of_sale_id=_string(value["point_of_sale_id"]),
        campaign_id=_string(value["campaign_id"]),
    )


def _principal(value):
    value = _object(value, _fields(AuthenticatedPrincipal))
    return AuthenticatedPrincipal(
        issuer=_string(value["issuer"]),
        subject=_string(value["subject"]),
    )


def decode_product001_mvp1_decision(payload):
    payload = _object(
        payload,
        _fields(Product001CommercialApprovalDecision),
    )
    return Product001CommercialApprovalDecision(
        decision_id=_string(payload["decision_id"]),
        document_identity=_identity(
            payload["document_identity"]
        ),
        document_scope=_scope(payload["document_scope"]),
        version_binding=_binding(payload["version_binding"]),
        principal=_principal(payload["principal"]),
        authorization_grant_id=_string(
            payload["authorization_grant_id"]
        ),
        decision=_enum(
            Product001CommercialDecision,
            payload["decision"],
        ),
        decided_at=_integer(payload["decided_at"]),
        evidence_reference=_string(
            payload["evidence_reference"]
        ),
    )


def _decode_signature(value):
    encoded = _string(value)

    try:
        signature = base64.b64decode(
            encoded,
            validate=True,
        )
    except (ValueError, binascii.Error) as exc:
        raise ValueError("invalid signature encoding") from exc

    if len(signature) != 64:
        raise ValueError("invalid signature length")

    if base64.b64encode(signature).decode("ascii") != encoded:
        raise ValueError("noncanonical signature encoding")

    return signature


def decode_product001_mvp1_authorization(payload):
    payload = _object(payload, ("signature_b64",))
    return MVP1Authorization(signature=_decode_signature(payload["signature_b64"]))


def decode_product001_mvp1_commitment_certificate(payload):
    """Decode V1 wire data for later verification against Gate-owned trust."""
    payload = _object(payload, ("version", "context", "signature_b64"))
    if _integer(payload["version"]) != 1:
        raise ValueError("unsupported commitment certificate version")
    context = _object(payload["context"], _fields(CommitmentContextV1))
    return CommitmentCertificateV1(
        context=CommitmentContextV1(**context),
        signature=_decode_signature(payload["signature_b64"]),
    )
