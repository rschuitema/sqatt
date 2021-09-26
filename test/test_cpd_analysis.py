from unittest.mock import patch

import pytest

from src.cpd.cpd_analysis import measure_code_duplication, measure_lines_of_code, determine_duplicate_lines_of_code


@patch("os.path.exists")
@patch("src.cpd.cpd_analysis.Subprocess")
def test_measure_code_duplication_calls_cpd_with_correct_parameters(subprocess_mock, exists_mock):
    """Test that cpd is called with the correct parameters to measure code duplication."""

    # arrange
    settings = {
        "report_directory": "/report_root/reports",
        "language": "python",
        "tokens": 123,
        "analysis_directory": "input_root/source",
    }

    exists_mock.return_value = True

    # act
    measure_code_duplication(settings)

    # assert
    subprocess_mock.assert_called_with(
        [
            "cpd",
            "--language",
            settings["language"],
            "--minimum-tokens",
            settings["tokens"],
            "--format",
            "csv",
            "--files",
            settings["analysis_directory"],
        ],
        verbose=1,
    )


@patch("os.path.exists")
@patch("src.cpd.cpd_analysis.Subprocess")
def test_measure_lines_of_code_calls_cloc_with_correct_parameters(subprocess_mock, exists_mock):
    """Test that cloc is called with the correct parameters to measure the lines of code."""

    # arrange
    settings = {
        "report_directory": "/report_root/reports",
        "language": "Java",
        "tokens": 11,
        "analysis_directory": "input_root/source",
    }

    exists_mock.return_value = True

    # act
    measure_lines_of_code(settings)

    # assert
    subprocess_mock.assert_called_with(
        [
            "cloc",
            "--csv",
            "--hide-rate",
            "--quiet",
            "--exclude-dir=test,tst",
            settings["analysis_directory"],
        ],
        verbose=1,
    )


def test_determine_duplicated_loc_calculates_correct_number_of_duplicated_lines():
    """Test that the number of duplicated lines of code is calculated correctly."""

    # arrange
    data = (
        "lines,tokens,occurrences\n"
        "40, 84, 2, 210,\west\west_dotcover.py, 19,\west\west_resharper_profile.py\n"
        "15, 78, 2, 76,\west\west_riskmatrix.py, 105,\west\west_riskmatrix.py\n"
        "34, 82, 3, 213,\west\west_dotcover.py, 7,\west\west_reporting.py, 22, \west\wet_resharper.py\n"
    )

    # act
    duplicated_loc = int(determine_duplicate_lines_of_code(data))

    # assert
    assert duplicated_loc == 212


def test_determine_duplicated_loc_returns_0_when_provided_string_is_empty():
    """Test that 0 is returned when the provided string is empty."""

    # arrange
    data = ""

    # act
    duplicated_loc = int(determine_duplicate_lines_of_code(data))

    # assert
    assert duplicated_loc == 0


def test_determine_duplicated_loc_raises_exception_when_provided_string_is_corrupt():
    """Test that 0 is returned when the provided string is empty."""

    # arrange
    data = "hello"

    # act & assert
    with pytest.raises(ValueError):
        determine_duplicate_lines_of_code(data)


def test_determine_duplicated_loc_raises_when_provided_string_has_wrong_header():
    """Test that 0 is returned when the provided string is has a wrong header."""

    # arrange
    data = (
        "hello,tokens,occurrences\n"
        "40, 84, 2, 210,\west\west_dotcover.py, 19,\west\west_resharper_profile.py\n"
        "15, 78, 2, 76,\west\west_riskmatrix.py, 105,\west\west_riskmatrix.py\n"
        "34, 82, 3, 213,\west\west_dotcover.py, 7,\west\west_reporting.py, 22, \west\wet_resharper.py\n"
    )

    # act & assert
    with pytest.raises(ValueError):
        determine_duplicate_lines_of_code(data)


def test_determine_duplicated_loc_raises_exception_when_lines_count_is_string():
    """Test that 0 is returned when the line_count is a string."""

    # arrange
    data = (
        "lines,tokens,occurrences\n"
        "40, 84, 2, 210,\west\west_dotcover.py, 19,\west\west_resharper_profile.py\n"
        "bla, 78, 2, 76,\west\west_riskmatrix.py, 105,\west\west_riskmatrix.py\n"
        "34, 82, 3, 213,\west\west_dotcover.py, 7,\west\west_reporting.py, 22, \west\wet_resharper.py\n"
    )

    # act & assert
    with pytest.raises(ValueError):
        determine_duplicate_lines_of_code(data)
