"""Unit test for cloc language analysis."""
from unittest.mock import patch, Mock, call

from src.cloc.cloc_languages import write_header


@patch("src.cloc.cloc_languages.csv")
def test_write_header(csv_mock):
    """Test that the correct header is written to the csv file."""

    csv_mock.writer = Mock(writerow=Mock())
    calls = [call.writerow(["Language", "Number Of Files", "Blank Lines", "Lines Of Code", "Comment Lines"])]
    write_header(csv_mock.writer)

    csv_mock.writer.writerow.assert_has_calls(calls)
