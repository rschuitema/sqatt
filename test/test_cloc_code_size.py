"""Unit test for cloc code size analysis."""
import csv

from io import StringIO
from unittest.mock import patch, Mock, call, mock_open

from src.cloc.cloc_code_size import calculate_test_code_to_production_code_ratio, calculate_comment_to_code_ratio, \
    write_code_size_header, write_code_size_metrics, get_size_metrics


def test_code_size_test_code_size_ratio_calculated_correctly():
    production_code_metrics = {"SUM": {"code": 120, "comment": 30}}
    test_code_metrics = {"SUM": {"code": 30, "comment": 10}}

    ratio = calculate_test_code_to_production_code_ratio(production_code_metrics, test_code_metrics)

    assert ratio == 30/120


def test_comment_to_code_ratio_calculated_correctly():

    production_code_metrics = {"SUM": {"code": 120, "comment": 30}}
    test_code_metrics = {"SUM": {"code": 30, "comment": 10}}
    ratio = calculate_comment_to_code_ratio(production_code_metrics, test_code_metrics)

    assert ratio == 40/150


@patch("src.cloc.cloc_code_size.csv")
def test_write_header(csv_mock):
    """Test that the correct header is written to the csv file."""

    csv_mock.writer = Mock(writerow=Mock())
    calls = [call.writerow(["Language", "Number Of Files", "Blank Lines", "Lines Of Code", "Comment Lines"])]
    write_code_size_header(csv_mock.writer)

    csv_mock.writer.writerow.assert_has_calls(calls)


@patch("src.cloc.cloc_code_size.csv")
def test_write_code_size_metrics(csv_mock):
    """Test that the correct metrics are written to the csv file."""

    metrics = {"Java": {"files": 201, "blank": 20, "code": 1003, "comment": 230},
               "C": {"files": 100, "blank": 7, "code": 1220, "comment": 30},
               "SUM": {"files": 301, "blank": 7, "code": 2120, "comment": 130}}

    csv_mock.writer = Mock(writerow=Mock())
    calls = [call.writerow(["Java", 201, 20, 1003, 230]), call.writerow(["C", 100, 7, 1220, 30]),
             call.writerow(["SUM", 301, 7, 2120, 130])]
    write_code_size_metrics(csv_mock.writer, metrics)

    csv_mock.writer.writerow.assert_has_calls(calls)


def test_get_size_metrics():

    data = StringIO(
        """language, files, blank, comment, code
        Java, 10, 11, 12, 13
    C, 20, 21, 22, 23
    SUM, 100, 200, 300, 400"""
    )

    report_file_name = r'code_sie_report.csv'
    test_reader = csv.DictReader(data, delimiter=",", skipinitialspace=True)
    with patch("src.cloc.cloc_code_size.open", mock_open()) as mocked_file:
        metrics = get_size_metrics(report_file_name, test_reader)

    mocked_file.assert_called_once_with(report_file_name, 'r', newline='\n')
    assert metrics["SUM"]["code"] == '400'
