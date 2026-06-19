from phase3.certificate_transparency.transparency_certificate_record import (
    TransparencyCertificateRecord,
)

from phase3.certificate_transparency.transparency_log import (
    TransparencyLog,
)

from phase3.certificate_transparency.transparency_query import (
    TransparencyQuery,
)


def test_query_returns_entry():

    log = TransparencyLog()

    entry = TransparencyCertificateRecord(
        entry_id="entry-001",
        certificate_id="cert-001",
    )

    log.add(entry)

    query = TransparencyQuery(log)

    result = query.by_id(
        "entry-001"
    )

    assert result == entry


def test_query_returns_none_for_missing():

    log = TransparencyLog()

    query = TransparencyQuery(log)

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_certificate_id():

    log = TransparencyLog()

    entry = TransparencyCertificateRecord(
        entry_id="entry-001",
        certificate_id="cert-001",
    )

    log.add(entry)

    query = TransparencyQuery(log)

    result = query.by_id(
        "entry-001"
    )

    assert (
        result.certificate_id
        == "cert-001"
    )
