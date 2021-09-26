from unittest.mock import patch

from src.cpd.cpd_analysis import measure_code_duplication, measure_lines_of_code


@patch("src.cpd.cpd_analysis.Subprocess")
def test_measure_code_duplication_calls_cpd_with_correct_parameters(subprocess_mock):
    """Test that cpd is called with the correct parameters to measure code duplication."""

    # arrange
    settings = {
        "report_directory": "/report_root/reports",
        "language": "python",
        "tokens": 123,
        "analysis_directory": "input_root/source",
    }

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


@patch("src.cpd.cpd_analysis.Subprocess")
def test_measure_lines_of_code_calls_cloc_with_correct_parameters(subprocess_mock):
    """Test that cloc is called with the correct parameters to measure the lines of code."""

    # arrange
    settings = {
        "report_directory": "/report_root/reports",
        "language": "Java",
        "tokens": 11,
        "analysis_directory": "input_root/source",
    }

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
