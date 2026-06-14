from epics.ztc25_formal_verification_certification.certification_report import (
    CertificationReport,
)


def test_report_contains_identifier():

    report = CertificationReport(
        report_id="report-001",
        obligations_checked=10,
        violations=0,
    )

    assert report.report_id == "report-001"


def test_report_contains_statistics():

    report = CertificationReport(
        report_id="report-001",
        obligations_checked=10,
        violations=2,
    )

    assert report.obligations_checked == 10
    assert report.violations == 2


def test_report_calculates_satisfied_obligations():

    report = CertificationReport(
        report_id="report-001",
        obligations_checked=10,
        violations=2,
    )

    assert report.satisfied() == 8


def test_report_serializes():

    report = CertificationReport(
        report_id="report-001",
        obligations_checked=10,
        violations=2,
    )

    assert report.to_dict() == {
        "report_id": "report-001",
        "obligations_checked": 10,
        "violations": 2,
        "satisfied": 8,
    }
