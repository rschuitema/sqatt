"""Unit test for lizard function size analysis."""
import csv
import os
from io import StringIO
from unittest.mock import patch, mock_open, call

import pytest

from src.lizard.lizard_analysis import determine_profiles, measure_function_metrics, create_profiles, parse_arguments

from src.profile.sqatt_profiles import (
    create_function_size_profile,
    create_complexity_profile,
    create_function_parameters_profile,
)


class LizardAnalysisMocks:
    """Collection of mocks for all analysis functions."""

    def __init__(self):
        """Create the analysis patches."""
        self.create_report_directory_patch = patch("src.lizard.lizard_analysis.create_report_directory")
        self.measure_function_metrics_patch = patch("src.lizard.lizard_analysis.measure_function_metrics")
        self.determine_profiles_patch = patch("src.lizard.lizard_analysis.determine_profiles")
        self.save_profile_patch = patch("src.profile.MetricProfile.MetricProfile.save")
        self.show_profile_patch = patch("src.lizard.lizard_analysis.show_profile")
        self.print_profile_patch = patch("src.profile.MetricProfile.MetricProfile.print")

        self.create_report_directory_mock = None
        self.measure_function_metrics_mock = None
        self.determine_profiles_mock = None
        self.show_profile_mock = None
        self.save_profile_mock = None
        self.print_profile_mock = None

    def start(self):
        """Start the patches."""

        self.create_report_directory_mock = self.create_report_directory_patch.start()
        self.measure_function_metrics_mock = self.measure_function_metrics_patch.start()
        self.determine_profiles_mock = self.determine_profiles_patch.start()
        self.show_profile_mock = self.show_profile_patch.start()
        self.save_profile_mock = self.save_profile_patch.start()
        self.print_profile_mock = self.print_profile_patch.start()

    def stop(self):
        """Stop the patches."""
        self.create_report_directory_patch.stop()
        self.measure_function_metrics_patch.stop()
        self.determine_profiles_patch.stop()
        self.show_profile_patch.stop()
        self.save_profile_patch.stop()
        self.print_profile_patch.stop()


@pytest.fixture
def lizard_analysis_mocks():
    """Fixture for creating analysis mocks."""

    mocks = LizardAnalysisMocks()
    mocks.start()
    yield mocks
    mocks.stop()


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


def test_option_all_performs_all_analysis(lizard_analysis_mocks):
    """Test that all analysis is performed when the --all option is provided."""

    # arrange
    args = parse_arguments(["/bla/input", "--all"])
    lizard_analysis_mocks.create_report_directory_mock.return_value = "test_reports"

    calls = [
        call.save(os.path.join("test_reports", "function_size_profile.csv")),
        call.save(os.path.join("test_reports", "complexity_profile.csv")),
        call.save(os.path.join("test_reports", "parameters_profile.csv")),
    ]

    # act
    args.func(args)

    # assert
    lizard_analysis_mocks.create_report_directory_mock.assert_called_once()
    lizard_analysis_mocks.measure_function_metrics_mock.assert_called_once()
    lizard_analysis_mocks.determine_profiles_mock.assert_called_once()

    lizard_analysis_mocks.save_profile_mock.has_calls(calls)
    assert lizard_analysis_mocks.show_profile_mock.call_count == 3
    assert lizard_analysis_mocks.print_profile_mock.call_count == 3


test_data = [
    ("--parameter", os.path.join("test_reports", "parameters_profile.csv")),
    ("--complexity", os.path.join("test_reports", "complexity_profile.csv")),
    ("--function-size", os.path.join("test_reports", "function_size_profile.csv")),
]


@pytest.mark.parametrize("option,expected_report_file", test_data)
def test_option_only_perform_specified_analysis(lizard_analysis_mocks, option, expected_report_file):
    """Test that only the analysis is performed that is specified."""

    # arrange
    args = parse_arguments(["/bla/input", option])
    lizard_analysis_mocks.create_report_directory_mock.return_value = "test_reports"

    # act
    args.func(args)

    # assert
    lizard_analysis_mocks.create_report_directory_mock.assert_called_once()
    lizard_analysis_mocks.measure_function_metrics_mock.assert_called_once()
    lizard_analysis_mocks.determine_profiles_mock.assert_called_once()
    lizard_analysis_mocks.show_profile_mock.assert_called_once()
    lizard_analysis_mocks.save_profile_mock.assert_called_once_with(expected_report_file)
    lizard_analysis_mocks.print_profile_mock.assert_called_once()


def test_option_output_has_correct_default(lizard_analysis_mocks):
    """Test that the default output directory is correct."""

    # arrange
    args = parse_arguments(["/bla/input", "--all"])

    # act
    args.func(args)

    # assert
    lizard_analysis_mocks.create_report_directory_mock.assert_called_with("./reports")


def test_option_output_has_correct_value(lizard_analysis_mocks):
    """Test that the default output directory is correct."""

    # arrange
    args = parse_arguments(["/bla/input", "--all", "--output=/bla/reports"])

    # act
    args.func(args)

    # assert
    lizard_analysis_mocks.create_report_directory_mock.assert_called_with("/bla/reports")
