"""Unit test for lizard function size analysis."""
import csv
import os
from io import StringIO
from unittest.mock import patch, mock_open

from src.lizard.lizard_analysis import determine_profiles, measure_function_metrics, create_profiles
from src.profile.sqatt_profiles import (
    create_function_size_profile,
    create_complexity_profile,
    create_function_parameters_profile,
)


def test_determine_function_size_profile():
    """Test if the function size profile is determined correctly."""

    # arrange
    profiles = {
        "function_size": create_function_size_profile(),
        "complexity": create_complexity_profile(),
        "parameters": create_function_parameters_profile(),
    }

    data = StringIO(
        """13,1,162,1,17,"add_analysis","analysis.py","add_analysis_parser","add_analysis_parser( subparsers )",27,43
           24,12,124,7,29,"add_metrics","analysis.py","add_metrics_parser","add_metrics_parser( subparsers )",46,74"""
    )

    report_file_name = r"function_size_report.csv"

    # act
    test_reader = csv.reader(data, delimiter=",", skipinitialspace=True)
    with patch("src.lizard.lizard_analysis.open", mock_open()) as mocked_file:
        determine_profiles(profiles, report_file_name, test_reader)

    # assert
    mocked_file.assert_called_once_with(report_file_name, "r", newline="\n", encoding="utf-8")

    assert profiles["function_size"].total_loc() == 37
    assert profiles["function_size"].regions()[0].loc() == 13
    assert profiles["function_size"].regions()[1].loc() == 24
    assert profiles["function_size"].regions()[2].loc() == 0
    assert profiles["function_size"].regions()[3].loc() == 0

    assert profiles["complexity"].total_loc() == 37
    assert profiles["complexity"].regions()[0].loc() == 13
    assert profiles["complexity"].regions()[1].loc() == 0
    assert profiles["complexity"].regions()[2].loc() == 24
    assert profiles["complexity"].regions()[3].loc() == 0

    assert profiles["parameters"].total_loc() == 37
    assert profiles["parameters"].regions()[0].loc() == 13
    assert profiles["parameters"].regions()[1].loc() == 0
    assert profiles["parameters"].regions()[2].loc() == 0
    assert profiles["parameters"].regions()[3].loc() == 24


@patch("src.reporting.reporting.create_report_directory")
@patch("src.lizard.lizard_analysis.Subprocess")
def test_measure_function_metrics(subprocess_mock, report_mock):
    """Test that the function metrics are measured."""

    # arrange
    input_dir = "/code/source"
    output_dir = "/bla/reports"
    output_file = os.path.join(output_dir, "function_metrics.csv")
    expected_command = ["lizard", "--csv", f"-o{output_file}", input_dir]

    report_mock.return_value = output_dir

    # act

    measure_function_metrics(input_dir, output_dir)

    # assert
    subprocess_mock.assert_called_with(expected_command, verbose=3)
    subprocess_mock.return_value.execute.assert_called_once()


def test_create_profiles():
    """Test that the correct set of profiles are created."""

    # arrange

    # act
    profiles = create_profiles()

    # assert
    assert len(list(profiles)) == 3
    assert profiles["function_size"].name() == "Function size"
    assert profiles["complexity"].name() == "Complexity"
    assert profiles["parameters"].name() == "Function parameters"
