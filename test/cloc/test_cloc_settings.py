"""Unit test for cloc analysis settings."""

from unittest.mock import mock_open, patch

import yaml

from src.cloc.cloc_settings import get_settings

DATA = """
production_filter: --exclude-dir=test,tst
test_filter: --match-d=(test|tst)
third_party_filter: --match-d=(external|ext)
generated_filter: --match-d=(generated|gen)
file_size_filter: --exclude-dir=test,tst

code_type: [
  production,
  test,
  third_party,
  generated,
]

report_directory: /projects/github/project/reports

analysis_directory: /projects/github/project
"""


@patch("builtins.open", mock_open())
@patch("src.cloc.cloc_settings.yaml.safe_load")
def test_settings_are_default_when_file_cannot_be_parsed(safe_load_mock):
    """Test that defaults settings are returned when there is an error parsing the file."""

    # arrange
    default_settings = {
        "analysis_directory": ".",
        "code_type": ["production", "test"],
        "production_filter": "--exclude-dir=test,tst",
        "test_filter": "--match-d=(test|tst)",
        "file_size_filter": "--exclude-dir=test,tst",
        "report_directory": "./reports",
    }

    # act

    safe_load_mock.side_effect = yaml.YAMLError
    settings = get_settings("/bla/config.yml", None, None)

    # assert
    assert settings == default_settings


def test_settings_are_default_when_configuration_file_does_not_exist():
    """Test that the specified output directory is used."""

    # arrange
    default_settings = {
        "analysis_directory": ".",
        "code_type": ["production", "test"],
        "production_filter": "--exclude-dir=test,tst",
        "test_filter": "--match-d=(test|tst)",
        "file_size_filter": "--exclude-dir=test,tst",
        "report_directory": "./reports",
    }

    # act
    with patch("src.cloc.cloc_settings.open", mock_open()) as mocked_open:
        mocked_open.side_effect = OSError
        settings = get_settings("None", None, None)

    # assert
    assert settings == default_settings


@patch("builtins.open", mock_open(read_data=DATA))
def test_report_directory_specified_overrules_configuration_file():
    """Test that the specified report directory is used."""

    # arrange
    expected_settings = {
        "analysis_directory": "/projects/github/project",
        "code_type": ["production", "test", "third_party", "generated"],
        "production_filter": "--exclude-dir=test,tst",
        "test_filter": "--match-d=(test|tst)",
        "third_party_filter": "--match-d=(external|ext)",
        "generated_filter": "--match-d=(generated|gen)",
        "file_size_filter": "--exclude-dir=test,tst",
        "report_directory": "/bla/reports",
    }

    # act
    settings = get_settings("/bla/config.yml", "/bla/reports", None)

    # assert
    assert settings == expected_settings


def test_report_directory_specified_overrules_default():
    """Test that the specified output directory is used."""

    # arrange
    expected_settings = {
        "analysis_directory": ".",
        "code_type": ["production", "test"],
        "production_filter": "--exclude-dir=test,tst",
        "test_filter": "--match-d=(test|tst)",
        "file_size_filter": "--exclude-dir=test,tst",
        "report_directory": "/bla/reports",
    }

    # act
    with patch("src.cloc.cloc_settings.open", mock_open()) as mocked_open:
        mocked_open.side_effect = OSError
        settings = get_settings("/bla/config.yml", "/bla/reports", None)

    # assert
    assert settings == expected_settings


@patch("builtins.open", mock_open(read_data=DATA))
def test_analysis_directory_specified_overrules_configuration_file():
    """Test that the specified analysis directory is used."""

    # arrange
    expected_settings = {
        "analysis_directory": "/bla/input",
        "code_type": ["production", "test", "third_party", "generated"],
        "production_filter": "--exclude-dir=test,tst",
        "test_filter": "--match-d=(test|tst)",
        "third_party_filter": "--match-d=(external|ext)",
        "generated_filter": "--match-d=(generated|gen)",
        "file_size_filter": "--exclude-dir=test,tst",
        "report_directory": "/projects/github/project/reports",
    }

    # act
    settings = get_settings("/bla/config.yml", None, "/bla/input")

    # assert
    assert settings == expected_settings


def test_analysis_directory_specified_overrules_default():
    """Test that the specified analysis directory is used."""

    # arrange
    expected_settings = {
        "analysis_directory": "/bla/input",
        "code_type": ["production", "test"],
        "production_filter": "--exclude-dir=test,tst",
        "test_filter": "--match-d=(test|tst)",
        "file_size_filter": "--exclude-dir=test,tst",
        "report_directory": "./reports",
    }

    # act
    with patch("src.cloc.cloc_settings.open", mock_open()) as mocked_open:
        mocked_open.side_effect = OSError
        settings = get_settings("/bla/config.yml", None, "/bla/input")

    # assert
    assert settings == expected_settings
