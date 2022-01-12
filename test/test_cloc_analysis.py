"""Unit test for the commandline parser of the cloc analysis."""
import configparser
from unittest.mock import patch

import pytest

from src.cloc.cloc_analysis import parse_arguments, get_settings


class ClocAnalysisMocks:
    """Collection of mocks for all analysis functions."""

    def __init__(self):
        """Create the analysis patches."""
        self.code_size_patch = patch("src.cloc.cloc_analysis.analyze_code_size")
        self.file_size_patch = patch("src.cloc.cloc_analysis.analyze_file_size")
        self.language_size_patch = patch("src.cloc.cloc_analysis.analyze_language")
        self.code_size_mock = None
        self.file_size_mock = None
        self.language_size_mock = None

    def start(self):
        """Start the patches."""

        self.code_size_mock = self.code_size_patch.start()
        self.file_size_mock = self.file_size_patch.start()
        self.language_size_mock = self.language_size_patch.start()

    def stop(self):
        """Stop the patches."""
        self.code_size_patch.stop()
        self.file_size_patch.stop()
        self.language_size_patch.stop()


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
    args = parse_arguments(["/bla/input", "--code-size"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.code_size_mock.assert_called_once()
    assert not cloc_analysis_mocks.language_size_mock.called
    assert not cloc_analysis_mocks.file_size_mock.called


def test_option_language_performs_only_language_analysis(cloc_analysis_mocks):
    """Test that only the language analysis is performed when the --language option is provided."""

    # arrange
    args = parse_arguments(["/bla/input", "--language"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.language_size_mock.assert_called_once()
    assert not cloc_analysis_mocks.code_size_mock.called
    assert not cloc_analysis_mocks.file_size_mock.called


def test_option_file_size_performs_only_file_size_analysis(cloc_analysis_mocks):
    """Test that only the file size analysis is performed when the --file-size option is provided."""

    # arrange
    args = parse_arguments(["/bla/input", "--file-size"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.file_size_mock.assert_called_once()
    assert not cloc_analysis_mocks.code_size_mock.called
    assert not cloc_analysis_mocks.language_size_mock.called


def test_option_all_performs_all_analysis(cloc_analysis_mocks):
    """Test that only the code size analysis is performed when the --code-size option is provided."""

    # arrange
    args = parse_arguments(["/bla/input", "--all"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.code_size_mock.assert_called_once()
    cloc_analysis_mocks.language_size_mock.assert_called_once()
    cloc_analysis_mocks.file_size_mock.assert_called_once()


def test_option_output_has_correct_default(cloc_analysis_mocks):
    """Test that the default output directory is correct."""

    # arrange
    args = parse_arguments(["/bla/input", "--all"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.code_size_mock.assert_called_with({})


def test_option_output_has_correct_value(cloc_analysis_mocks):
    """Test that the default output directory is correct."""

    # arrange
    args = parse_arguments(["/bla/input", "--all", "--output=/bla/reports"])

    # act
    args.func(args)

    # assert
    cloc_analysis_mocks.code_size_mock.assert_called_with({})


@patch("os.path.exists")
def test_get_setting_returns_empty_settings_when_config_file_does_not_exist(path_exists_mock):
    """Test that the settings is empty when the config file does not exist."""

    # arrange
    path_exists_mock.return_value = False

    # act
    settings = get_settings("config.bla")

    # assert
    assert not settings


@patch("os.path.exists")
def test_get_setting_has_correct_code_types(path_exists_mock):
    """Test that the settings is empty when the config file does not exist."""

    # arrange
    path_exists_mock.return_value = True

    config = configparser.ConfigParser()
    config.add_section("code_type")
    config.add_section("filters")
    config.add_section("reporting")
    config.add_section("analysis")
    config.set("code_type", "production", "bla")
    config.set("code_type", "test", "bla")
    config.set("filters", "production_filter", "bla2")
    config.set("filters", "test_filter", "bla2")
    config.set("reporting", "directory", "bla3")
    config.set("analysis", "directory", "bla4")

    # act
    settings = get_settings("config.bla", config)

    # assert
    assert len(settings["code_type"]) == 2
    assert settings["code_type"] == ["production", "test"]
    assert settings["production_filter"] == "bla2"
    assert settings["test_filter"] == "bla2"
    assert settings["report_directory"] == "bla3"
    assert settings["analysis_directory"] == "bla4"
