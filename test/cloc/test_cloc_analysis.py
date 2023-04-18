"""Unit test for the commandline parser of the cloc analysis."""

# pylint: disable=redefined-outer-name
from unittest.mock import patch

import pytest

from src.cloc.cloc_analysis import parse_arguments


class ClocAnalysisMocks:
    """Collection of mocks for all analysis functions."""

    def __init__(self):
        """Create the analysis patches."""
        self.code_volume_patch = patch("src.cloc.cloc_analysis.analyze_code_volume")
        self.code_type_patch = patch("src.cloc.cloc_analysis.analyze_code_type")
        self.file_size_patch = patch("src.cloc.cloc_analysis.analyze_file_size")
        self.language_size_patch = patch("src.cloc.cloc_analysis.analyze_language")

        self.code_volume_mock = None
        self.code_type_mock = None
        self.file_size_mock = None
        self.language_size_mock = None

    def start(self):
        """Start the patches."""

        self.code_volume_mock = self.code_volume_patch.start()
        self.code_type_mock = self.code_type_patch.start()
        self.file_size_mock = self.file_size_patch.start()
        self.language_size_mock = self.language_size_patch.start()

    def stop(self):
        """Stop the patches."""
        self.code_volume_patch.stop()
        self.code_type_patch.stop()
        self.file_size_patch.stop()
        self.language_size_patch.stop()


@pytest.fixture
def cloc_analysis_mocks():
    """Fixture for creating analysis mocks."""

    mocks = ClocAnalysisMocks()
    mocks.start()
    yield mocks
    mocks.stop()


def test_option_language_performs_only_language_analysis(cloc_analysis_mocks):
    """Test that only the language analysis is performed when the --language option is provided."""

    # arrange
    args = parse_arguments(["/bla/input", "--language"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.language_size_mock.assert_called_once()
    cloc_analysis_mocks.file_size_mock.assert_not_called()
    cloc_analysis_mocks.code_volume_mock.assert_not_called()
    cloc_analysis_mocks.code_type_mock.assert_not_called()


def test_option_file_size_performs_only_file_size_analysis(cloc_analysis_mocks):
    """Test that only the file size analysis is performed when the --file-size option is provided."""

    # arrange
    args = parse_arguments(["/bla/input", "--file-size"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.file_size_mock.assert_called_once()
    cloc_analysis_mocks.code_volume_mock.assert_not_called()
    cloc_analysis_mocks.code_type_mock.assert_not_called()
    cloc_analysis_mocks.language_size_mock.assert_not_called()


def test_option_code_volume_performs_code_type_and_volume_analysis(cloc_analysis_mocks):
    """Test that code volume and code type analysis is performed when the --code-volume option is provided."""

    # arrange
    args = parse_arguments(["/bla/input", "--code-volume"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.code_type_mock.assert_called_once()
    cloc_analysis_mocks.code_volume_mock.assert_called_once()
    cloc_analysis_mocks.language_size_mock.assert_not_called()
    cloc_analysis_mocks.file_size_mock.assert_not_called()


def test_option_code_type_performs_only_code_type_analysis(cloc_analysis_mocks):
    """Test that only the code type analysis is performed when the --code-type option is provided."""

    # arrange
    args = parse_arguments(["/bla/input", "--code-type"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.code_type_mock.assert_called_once()
    cloc_analysis_mocks.language_size_mock.assert_not_called()
    cloc_analysis_mocks.file_size_mock.assert_not_called()
    cloc_analysis_mocks.code_volume_mock.assert_not_called()


def test_option_all_performs_all_analysis(cloc_analysis_mocks):
    """Test that all the analysis is performed when the --all option is provided."""

    # arrange
    args = parse_arguments(["/bla/input", "--all"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.code_volume_mock.assert_called_once()
    cloc_analysis_mocks.code_type_mock.assert_called_once()
    cloc_analysis_mocks.language_size_mock.assert_called_once()
    cloc_analysis_mocks.file_size_mock.assert_called_once()
