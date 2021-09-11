"""Unit test for cloc code size analysis."""
from unittest.mock import patch, Mock, call, mock_open

from src.cloc.cloc_code_size import (
    calculate_test_code_to_production_code_ratio,
    calculate_comment_to_code_ratio,
    write_code_size_header,
    write_code_size_metrics,
    save_code_metrics,
    analyze_size,
)


def test_code_size_test_code_size_ratio_calculated_correctly():
    production_code_metrics = {"SUM": {"code": 120, "comment": 30}}
    test_code_metrics = {"SUM": {"code": 30, "comment": 10}}

    ratio = calculate_test_code_to_production_code_ratio(production_code_metrics, test_code_metrics)

    assert ratio == 30 / 120


def test_comment_to_code_ratio_calculated_correctly():

    production_code_metrics = {"SUM": {"code": 120, "comment": 30}}
    test_code_metrics = {"SUM": {"code": 30, "comment": 10}}
    ratio = calculate_comment_to_code_ratio(production_code_metrics, test_code_metrics)

    assert ratio == 40 / 150


@patch("src.cloc.cloc_code_size.csv")
def test_write_header(csv_mock):
    """Test that the correct header is written to the csv file."""

    csv_mock.writer = Mock(writerow=Mock())
    calls = [call.writerow(["Blank Lines", "Lines Of Code", "Comment Lines"])]
    write_code_size_header(csv_mock.writer)

    csv_mock.writer.writerow.assert_has_calls(calls)


@patch("src.cloc.cloc_code_size.csv")
def test_write_code_size_metrics(csv_mock):
    """Test that the correct metrics are written to the csv file."""

    metrics = {
        "Java": {"files": 201, "blank": 20, "code": 1003, "comment": 230},
        "C": {"files": 100, "blank": 7, "code": 1220, "comment": 30},
        "SUM": {"files": 301, "blank": 7, "code": 2120, "comment": 130},
    }

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow([7, 2120, 130]),
    ]
    write_code_size_metrics(csv_mock.writer, metrics)

    csv_mock.writer.writerow.assert_has_calls(calls)


@patch("src.cloc.cloc_code_size.csv")
def test_save_metrics(csv_mock):
    production_code_size_file = "code_size.csv"

    production_code_metrics = {
        "Java": {"files": 201, "blank": 20, "code": 1003, "comment": 230},
        "C#": {"files": 100, "blank": 7, "code": 1220, "comment": 30},
        "SUM": {"files": 301, "blank": 7, "code": 2120, "comment": 130},
    }

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow(["Blank Lines", "Lines Of Code", "Comment Lines"]),
        call.writerow([7, 2120, 130]),
    ]
    with patch("src.cloc.cloc_code_size.open", mock_open()) as mocked_file:
        save_code_metrics(production_code_size_file, production_code_metrics)

        mocked_file.assert_called_once_with(production_code_size_file, "w", encoding="utf-8")
        csv_mock.writer().assert_has_calls(calls)


@patch("src.reporting.reporting.create_report_directory")
def test_metrics_are_empty_when_no_code_type_specified(create_report_directory_mock):
    # arrange
    settings = {"report_directory": "./reports", "code_type": ""}

    create_report_directory_mock.return_value = settings["report_directory"]

    # act
    metrics = analyze_size(settings)

    # assert
    assert len(metrics) == 0
