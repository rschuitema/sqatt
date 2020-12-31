from unittest.mock import patch

import pytest

from src.lizard.lizard_analysis import parse_arguments


class LizardAnalysisMocks:
    """Collection of mocks for all analysis functions."""

    def __init__(self):
        """Create the analysis patches."""
        self.function_size_patch = patch("src.lizard.lizard_analysis.analyze_function_size")
        self.complexity_patch = patch("src.lizard.lizard_analysis.analyze_complexity")
        self.function_parameters_patch = patch("src.lizard.lizard_analysis.analyze_function_parameters")
        self.function_size_mock = None
        self.complexity_mock = None
        self.function_parameters_mock = None

    def start(self):
        """Start the patches."""

        self.function_size_mock = self.function_size_patch.start()
        self.complexity_mock = self.complexity_patch.start()
        self.function_parameters_mock = self.function_parameters_patch.start()

    def stop(self):
        """Stop the patches."""
        self.function_size_mock.stop()
        self.complexity_mock.stop()
        self.function_parameters_mock.stop()


@pytest.fixture
def lizard_analysis_mocks():
    """Fixture for creating analysis mocks."""

    mocks = LizardAnalysisMocks()
    mocks.start()
    yield mocks
    mocks.stop()


def test_option_output_has_correct_default(lizard_analysis_mocks):
    """Test that the default output directory is correct."""

    # arrange
    args = parse_arguments(["analysis", "/tmp/input", "--all"])

    # act
    args.func(args)

    # assert
    lizard_analysis_mocks.function_size_mock.assert_called_with("/tmp/input", "./reports")
    lizard_analysis_mocks.complexity_mock.assert_called_with("/tmp/input", "./reports")
    lizard_analysis_mocks.function_parameters_mock.assert_called_with("/tmp/input", "./reports")


def test_option_all_performs_all_analysis(lizard_analysis_mocks):
    """Test that only the code size analysis is performed when the --code-size option is provided."""

    # arrange
    args = parse_arguments(["analysis", "/tmp/input", "--all", "--output=/tmp/reports"])

    # act
    args.func(args)

    # assert
    lizard_analysis_mocks.function_size_mock.assert_called_with("/tmp/input", "/tmp/reports")
    lizard_analysis_mocks.complexity_mock.assert_called_with("/tmp/input", "/tmp/reports")
    lizard_analysis_mocks.function_parameters_mock.assert_called_with("/tmp/input", "/tmp/reports")


def test_option_function_size_collects_only_function_size_metrics(lizard_analysis_mocks):
    """Test that only the function size metrics are collected when the --function-size option is provided."""

    # arrange
    args = parse_arguments(["analysis", "--function-size", "/tmp/input"])

    # act
    args.func(args)

    # assert
    lizard_analysis_mocks.function_size_mock.assert_called_once()
    lizard_analysis_mocks.complexity_mock.assert_not_called()
    lizard_analysis_mocks.function_parameters_mock.assert_not_called()


def test_option_complexity_collects_only_complexity_metrics(lizard_analysis_mocks):
    """Test that only the function size metrics are collected when the --function-size option is provided."""

    # arrange
    args = parse_arguments(["analysis", "--complexity", "/tmp/input"])

    # act
    args.func(args)

    # assert
    lizard_analysis_mocks.function_size_mock.assert_not_called()
    lizard_analysis_mocks.complexity_mock.assert_called_once()
    lizard_analysis_mocks.function_parameters_mock.assert_not_called()


def test_option_function_parameters_collects_only_function_parameters_metrics(lizard_analysis_mocks):
    """Test that only the function size metrics are collected when the --function-size option is provided."""

    # arrange
    args = parse_arguments(["analysis", "--interface", "/tmp/input"])

    # act
    args.func(args)

    # assert
    lizard_analysis_mocks.function_size_mock.assert_not_called()
    lizard_analysis_mocks.complexity_mock.assert_not_called()
    lizard_analysis_mocks.function_parameters_mock.assert_called_once()
