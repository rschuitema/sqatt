"""Unit test for cloc language analysis."""
from unittest.mock import patch, Mock, call, mock_open

from src.cloc.cloc_languages import write_header, write_metrics


@patch("src.cloc.cloc_languages.csv")
def test_write_header(csv_mock):
    """Test that the correct header is written to the csv file."""

    # arrange
    csv_mock.writer = Mock(writerow=Mock())
    calls = [call.writerow(["Language", "Number Of Files", "Blank Lines", "Lines Of Code", "Comment Lines"])]

    # act
    write_header(csv_mock.writer)

    # assert
    csv_mock.writer.writerow.assert_has_calls(calls)


@patch("src.cloc.cloc_languages.csv")
def test_write_metrics(csv_mock):
    """Test that the metrics are written correctly to file."""

    # arrange
    production_code_metrics = {
        "Python": {"files": 201, "blank": 20, "code": 1003, "comment": 230},
        "C#": {"files": 100, "blank": 7, "code": 1220, "comment": 30},
    }

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow(["Python", 201, 20, 1003, 230]),
        call.writerow(["C#", 100, 7, 1220, 30]),
    ]

    # act
    write_metrics(csv_mock.writer, production_code_metrics)

    # assert
    csv_mock.writer.assert_has_calls(calls)
