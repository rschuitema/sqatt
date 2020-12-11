"""Unit test for the commandline parser of the cloc analysis."""
from unittest.mock import patch

import pytest

from src.cloc.cloc_analysis import parse_arguments


class ClocAnalysisMocks:
    """Collection of mocks for all analysis functions."""

    def __init__(self):
        """Create the analysis patches."""
        self.code_size_patch = patch("src.cloc.cloc_analysis.analyze_code_size")
        self.code_size_mock = None

    def start(self):
        """Start the patches."""

        self.code_size_mock = self.code_size_patch.start()

    def stop(self):
        """Stop the patches."""
        self.code_size_patch.stop()


@pytest.fixture
def cloc_analysis_mocks():
    """Fixture for creating analysis mocks."""

    mocks = ClocAnalysisMocks()
    mocks.start()
    yield mocks
    mocks.stop()


def test_option_code_size_performs_only_code_size_analysis(cloc_analysis_mocks):
    """Test that only the code size analysis is performed when the --code-size option is provided."""

    # arrange
    args = parse_arguments(["analysis", "/tmp/input", "--code-size"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.code_size_mock.assert_called_once()


def test_option_all_performs_all_analysis(cloc_analysis_mocks):
    """Test that only the code size analysis is performed when the --code-size option is provided."""

    # arrange
    args = parse_arguments(["analysis", "/tmp/input", "--all"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.code_size_mock.assert_called_once()


def test_option_output_has_correct_default(cloc_analysis_mocks):
    """Test that the default output directory is correct."""

    # arrange
    args = parse_arguments(["analysis", "/tmp/input", "--all"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.code_size_mock.assert_called_with("/tmp/input", "./reports")


def test_option_output_has_correct_value(cloc_analysis_mocks):
    """Test that the default output directory is correct."""

    # arrange
    args = parse_arguments(["analysis", "/tmp/input", "--all", "--output=/tmp/reports"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.code_size_mock.assert_called_with("/tmp/input", "/tmp/reports")
