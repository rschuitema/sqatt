"""Unit test for cloc code size analysis."""
import csv
from io import StringIO
from unittest.mock import patch, mock_open

from src.lizard.lizard_function_size import determine_function_size_profile
from src.profile.MetricProfile import MetricProfile
from src.profile.MetricRegion import MetricRegion


def test_determine_function_size_profile():
    """Test if the function size profile is determined correctly."""

    # arrange
    regions = [
        MetricRegion("0-15", 0, 16),
        MetricRegion("16-30", 15, 31),
        MetricRegion("31-60", 30, 61),
        MetricRegion("60+", 60, 1001),
    ]

    profile = MetricProfile("Function size", regions)

    data = StringIO(
        """13,1,162,1,17,"add_analysis","analysis.py","add_analysis_parser","add_analysis_parser( subparsers )",27,43
           24,1,124,1,29,"add_metrics","analysis.py","add_metrics_parser","add_metrics_parser( subparsers )",46,74"""
    )

    report_file_name = r"function_size_report.csv"

    # act
    test_reader = csv.reader(data, delimiter=",", skipinitialspace=True)
    with patch("src.lizard.lizard_function_size.open", mock_open()) as mocked_file:
        determine_function_size_profile(profile, report_file_name, test_reader)

    # assert
    mocked_file.assert_called_once_with(report_file_name, "r", newline="\n")

    assert profile.total_loc() == 37
    assert profile.regions()[0].loc() == 13
    assert profile.regions()[1].loc() == 24
    assert profile.regions()[2].loc() == 0
    assert profile.regions()[3].loc() == 0
