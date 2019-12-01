"""Unit test for the commandline parser of the understand analysis."""
from unittest.mock import patch, Mock

import sys
import pytest

sys.modules["understand"] = Mock()

from src.understand.understand_analysis import parse_arguments


# pylint: disable=too-many-instance-attributes
class AnalysisMocks:
    """Collection of mocks for all analysis functions."""

    def __init__(self):
        """Create the analysis patches."""

        self.code_size_patch = patch("src.understand.understand_analysis.analyze_code_size")
        self.complexity_patch = patch("src.understand.understand_analysis.analyze_complexity")
        self.fan_in_patch = patch("src.understand.understand_analysis.analyze_fan_in")
        self.fan_out_patch = patch("src.understand.understand_analysis.analyze_fan_out")
        self.function_size_patch = patch("src.understand.understand_analysis.analyze_function_size")
        self.file_size_patch = patch("src.understand.understand_analysis.analyze_file_size")
        self.interface_patch = patch("src.understand.understand_analysis.analyze_interface")
        self.code_size_mock = None
        self.complexity_mock = None
        self.fan_in_mock = None
        self.fan_out_mock = None
        self.function_size_mock = None
        self.file_size_mock = None
        self.interface_mock = None

    def start(self):
        """Start the patches."""

        self.code_size_mock = self.code_size_patch.start()
        self.complexity_mock = self.complexity_patch.start()
        self.fan_in_mock = self.fan_in_patch.start()
        self.fan_out_mock = self.fan_out_patch.start()
        self.function_size_mock = self.function_size_patch.start()
        self.file_size_mock = self.file_size_patch.start()
        self.interface_mock = self.interface_patch.start()

    def stop(self):
        """Stop the patches."""

        self.code_size_mock.stop()
        self.complexity_patch.stop()
        self.fan_in_patch.stop()
        self.fan_out_patch.stop()
        self.function_size_patch.stop()
        self.file_size_patch.stop()
        self.interface_patch.stop()


# pylint: enable=too-many-instance-attributes


@pytest.fixture
def analysis_mocks():
    """Fixture for creating analysis mocks."""

    mocks = AnalysisMocks()
    mocks.start()
    yield mocks
    mocks.stop()


class MetricsMocks:
    """Collection of mocks for metric collection functions."""

    def __init__(self):
        """Create the patches."""

        self.file_patch = patch("src.understand.understand_analysis.collect_file_metrics")
        self.function_patch = patch("src.understand.understand_analysis.collect_function_metrics")
        self.file_mock = None
        self.function_mock = None

    def start(self):
        """Start the patches."""

        self.file_mock = self.file_patch.start()
        self.function_mock = self.function_patch.start()

    def stop(self):
        """Stop the patches."""
        self.file_patch.stop()
        self.function_patch.stop()


@pytest.fixture
def metrics_mocks():
    """Fixture for the metric mocks."""

    mocks = MetricsMocks()
    mocks.start()
    yield mocks
    mocks.stop()


# pylint: disable=redefined-outer-name
def test_option_code_size_performs_only_code_size_analysis(analysis_mocks):
    """Test that only the code size analysis is performed when the --code-size option is provided."""

    # arrange
    args = parse_arguments(["analysis", "--code-size", "db"])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_called_once()
    analysis_mocks.complexity_mock.assert_not_called()
    analysis_mocks.fan_in_mock.assert_not_called()
    analysis_mocks.fan_out_mock.assert_not_called()
    analysis_mocks.function_size_mock.assert_not_called()
    analysis_mocks.file_size_mock.assert_not_called()
    analysis_mocks.interface_mock.assert_not_called()


def test_option_complexity_performs_only_complexity_analysis(analysis_mocks):
    """Test that only the complexity analysis is performed when the --complexity option is provided."""
    # arrange
    args = parse_arguments(["analysis", "--complexity", "db"])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_not_called()
    analysis_mocks.complexity_mock.assert_called_once()
    analysis_mocks.fan_in_mock.assert_not_called()
    analysis_mocks.fan_out_mock.assert_not_called()
    analysis_mocks.function_size_mock.assert_not_called()
    analysis_mocks.file_size_mock.assert_not_called()
    analysis_mocks.interface_mock.assert_not_called()


def test_option_fan_in_performs_only_fan_in_analysis(analysis_mocks):
    """Test that only the fan-in analysis is performed when the --fan-in option is provided."""

    # arrange
    args = parse_arguments(["analysis", "--fan-in", "db"])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_not_called()
    analysis_mocks.complexity_mock.assert_not_called()
    analysis_mocks.fan_in_mock.assert_called_once()
    analysis_mocks.fan_out_mock.assert_not_called()
    analysis_mocks.function_size_mock.assert_not_called()
    analysis_mocks.file_size_mock.assert_not_called()
    analysis_mocks.interface_mock.assert_not_called()


def test_option_fan_out_performs_only_fan_out_analysis(analysis_mocks):
    """Test that only the fan-out analysis is performed when the --fan-out option is provided."""

    # arrange
    args = parse_arguments(["analysis", "--fan-out", "db"])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_not_called()
    analysis_mocks.complexity_mock.assert_not_called()
    analysis_mocks.fan_in_mock.assert_not_called()
    analysis_mocks.fan_out_mock.assert_called_once()
    analysis_mocks.function_size_mock.assert_not_called()
    analysis_mocks.file_size_mock.assert_not_called()
    analysis_mocks.interface_mock.assert_not_called()


def test_option_function_size_performs_only_function_size_analysis(analysis_mocks):
    """Test that only the function size analysis is performed when the --function-size option is provided."""

    # arrange
    args = parse_arguments(["analysis", "--function-size", "db"])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_not_called()
    analysis_mocks.complexity_mock.assert_not_called()
    analysis_mocks.fan_in_mock.assert_not_called()
    analysis_mocks.fan_out_mock.assert_not_called()
    analysis_mocks.function_size_mock.assert_called_once()
    analysis_mocks.file_size_mock.assert_not_called()
    analysis_mocks.interface_mock.assert_not_called()


def test_option_file_size_performs_only_file_size_analysis(analysis_mocks):
    """Test that only the file size analysis is performed when the --file-size option is provided."""

    # arrange
    args = parse_arguments(["analysis", "--file-size", "db"])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_not_called()
    analysis_mocks.complexity_mock.assert_not_called()
    analysis_mocks.fan_in_mock.assert_not_called()
    analysis_mocks.fan_out_mock.assert_not_called()
    analysis_mocks.function_size_mock.assert_not_called()
    analysis_mocks.file_size_mock.assert_called_once()
    analysis_mocks.interface_mock.assert_not_called()


def test_option_interface_performs_only_interface_analysis(analysis_mocks):
    """Test that only the interface analysis is performed when the --interface option is provided."""

    # arrange
    args = parse_arguments(["analysis", "--interface", "db"])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_not_called()
    analysis_mocks.complexity_mock.assert_not_called()
    analysis_mocks.fan_in_mock.assert_not_called()
    analysis_mocks.fan_out_mock.assert_not_called()
    analysis_mocks.function_size_mock.assert_not_called()
    analysis_mocks.file_size_mock.assert_not_called()
    analysis_mocks.interface_mock.assert_called_once()


def test_option_all_performs_all_analysis(analysis_mocks):
    """Test that all analysis is performed when the --all option is provided."""

    # arrange
    args = parse_arguments(["analysis", "--all", "db"])

    # act
    args.func(args)

    # assert
    analysis_mocks.code_size_mock.assert_called_once()
    analysis_mocks.complexity_mock.assert_called_once()
    analysis_mocks.fan_in_mock.assert_called_once()
    analysis_mocks.fan_out_mock.assert_called_once()
    analysis_mocks.function_size_mock.assert_called_once()
    analysis_mocks.file_size_mock.assert_called_once()
    analysis_mocks.interface_mock.assert_called_once()


def test_option_file_collects_only_file_metrics(metrics_mocks):
    """Test that only the file metrics are collected when the --file option is provided."""

    # arrange
    args = parse_arguments(["metrics", "--file", "db"])

    # act
    args.func(args)

    # assert
    metrics_mocks.file_mock.assert_called_once()
    metrics_mocks.function_mock.assert_not_called()


def test_option_file_should_have_correct_default_values(metrics_mocks):
    """Test that the options for file have correct default values."""

    # arrange
    args = parse_arguments(["metrics", "--file", "db"])

    # act
    args.func(args)

    # assert
    metrics_mocks.file_mock.assert_called_with("db", "./reports", None, None)


def test_options_file_should_have_correct_values(metrics_mocks):
    """Test that the options for file have correct provided values."""

    # arrange
    args = parse_arguments(["metrics", "--file", "--output=/tmp/reports", "--module=foo", "--sort=CountLine", "db"])

    # act
    args.func(args)

    # assert
    metrics_mocks.file_mock.assert_called_with("db", "/tmp/reports", "foo", "CountLine")


def test_option_function_collects_only_function_metrics(metrics_mocks):
    """Test that only the function metrics are collected when the --function option is provided."""

    # arrange
    args = parse_arguments(["metrics", "--function", "db"])

    # act
    args.func(args)

    # assert
    metrics_mocks.file_mock.assert_not_called()
    metrics_mocks.function_mock.assert_called_once()


# pylint: enable=redefined-outer-name
