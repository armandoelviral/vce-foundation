from epics.ztc23_security_validation_framework.security_validation_report import (
    SecurityValidationReport,
)


def test_report_contains_identifier():

    report = SecurityValidationReport(
        report_id="report-001",
        total_tests=10,
        failures=0,
    )

    assert report.report_id == "report-001"


def test_report_contains_test_statistics():

    report = SecurityValidationReport(
        report_id="report-001",
        total_tests=10,
        failures=2,
    )

    assert report.total_tests == 10
    assert report.failures == 2


def test_report_calculates_successful_tests():

    report = SecurityValidationReport(
        report_id="report-001",
        total_tests=10,
        failures=2,
    )

    assert report.successes() == 8


def test_report_serializes():

    report = SecurityValidationReport(
        report_id="report-001",
        total_tests=10,
        failures=2,
    )

    assert report.to_dict() == {
        "report_id": "report-001",
        "total_tests": 10,
        "failures": 2,
        "successes": 8,
    }
