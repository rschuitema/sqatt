"""Unit test for cloc code size analysis."""

import csv
from io import StringIO
from unittest.mock import patch, mock_open
from src.cloc.cloc_measure import get_size_metrics, measure_lines_of_code


def test_get_size_metrics():
    """Test that the size metrics can be retrieved from file."""

    data = StringIO(
        """language, files, blank, comment, code
        Java, 10, 11, 12, 13
    C, 20, 21, 22, 23
    SUM, 100, 200, 300, 400"""
    )

    report_file_name = r"code_size_report.csv"
    test_reader = csv.DictReader(data, delimiter=",", skipinitialspace=True)
    with patch("src.cloc.cloc_measure.open", mock_open()) as mocked_file:
        metrics = get_size_metrics(report_file_name, test_reader)

    mocked_file.assert_called_once_with(report_file_name, "r", newline="\n", encoding="utf-8")
    assert metrics["C"]["code"] == "23"


@patch("src.cloc.cloc_measure.Subprocess")
def test_measure_lines_of_code_calls_cloc_with_correct_parameters(subprocess_mock):
    """Test that cloc is called with the correct parameters to measure the lines of code."""

    # arrange
    input_dir = "/test_root/test_dir"
    report_file = "my_report"
    measure_filter = "my_filter"

    # act
    measure_lines_of_code(input_dir, report_file, measure_filter)

    # assert
    subprocess_mock.assert_called_with(
        [
            "cloc",
            "--csv",
            "--csv-delimiter=,",
            "--hide-rate",
            f"--report-file={report_file}",
            measure_filter,
            input_dir,
        ],
        verbose=1,
    )
