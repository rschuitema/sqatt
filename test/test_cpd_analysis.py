from unittest.mock import patch, Mock, ANY, call, mock_open

import pytest

from src.cpd.cpd_analysis import (
    measure_code_duplication,
    measure_lines_of_code,
    determine_duplicate_lines_of_code,
    determine_colors,
    determine_total_lines_of_code,
    show_duplication_profile,
    parse_arguments,
    get_settings,
    save_duplication_profile,
)


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


def test_determine_total_lines_of_code_is_correct():
    """Test if the correct number of total lines of code is determined."""

    # arrange
    data = (
        "\n"
        'files,language,blank,comment,code,"github.com/AlDanial/cloc v 1.82"\n'
        "58,Python,992,495,2178\n"
        "2,Cucumber,10,0,79\n"
        "81,SUM,1066,500,5003\n"
    )

    # act
    total_loc = int(determine_total_lines_of_code(data))

    # assert
    assert total_loc == 5003


def test_determine_total_lines_of_code_is_0_when_provided_empty_string():
    """Test if the total lines of code is 0 when provide an empty string."""

    # arrange
    data = "\n"

    # act
    total_loc = int(determine_total_lines_of_code(data))

    # assert
    assert total_loc == 0


def test_determine_total_lines_of_code_is_0_when_sum_not_in_string():
    """Test if the total lines of code is 0 when sum not in string."""

    # arrange
    data = (
        "\n"
        'files,language,blank,comment,code,"github.com/AlDanial/cloc v 1.82"\n'
        "58,Java,992,495,2178\n"
        "2,Cucumber,10,0,79\n"
    )

    # act
    total_loc = int(determine_total_lines_of_code(data))

    # assert
    assert total_loc == 0


TEST_DATA = [
    (0, ["rgb(204, 5, 5)", "rgb(121, 185, 79)"]),
    (3, ["rgb(121, 185, 79)", "rgb(121, 185, 79)"]),
    (4, ["rgb(255, 204, 5)", "rgb(121, 185, 79)"]),
    (5, ["rgb(255, 204, 5)", "rgb(121, 185, 79)"]),
    (19, ["rgb(251, 135, 56)", "rgb(121, 185, 79)"]),
    (20, ["rgb(251, 135, 56)", "rgb(121, 185, 79)"]),
    (21, ["rgb(204, 5, 5)", "rgb(121, 185, 79)"]),
]


@pytest.mark.parametrize("percentage,expected_colors", TEST_DATA)
def test_determine_colors(percentage, expected_colors):
    """Test that the correct colors are determine from the percentage."""

    # arrange

    # act
    colors = determine_colors(percentage)

    # assert
    assert colors == expected_colors
    assert len(colors) == 2


@patch("src.profile.show.go.Figure")
def test_show_duplication_profile_figure_created_with_correct_values(figure_mock):
    """Test that the figure is created with the correct values."""

    # arrange

    # act
    with patch("src.profile.show.go.Pie") as pie_mock:
        figure_mock.show = Mock()
        show_duplication_profile(1000, 450)

    # assert
    pie_mock.assert_called_once_with(
        title={"text": "Code duplication"},
        labels=["Duplicated code", "Non duplicated code"],
        values=[450, 550],
        hole=ANY,
        marker_line=ANY,
        marker_colors=ANY,
    )

    figure_mock().show.assert_called_once()


@patch("os.path.join")
def test_options_have_correct_default(os_path_join_mock):
    """Test that the default output directory is correct."""

    # arrange
    os_path_join_mock.return_value = "/bin/reports"

    args = parse_arguments(["/bla/input"])

    expected_defaults = {
        "tokens": 100,
        "language": "python",
        "report_directory": "/bin/reports",
        "analysis_directory": "/bla/input",
    }

    # act
    settings = get_settings(args)

    # assert
    assert settings == expected_defaults


def test_options_have_correct_value():
    """Test that the default output directory is correct."""

    # arrange
    args = parse_arguments(["/bla/input", "--tokens=16", "--language=java", "--output=/bin/reports"])
    expected_defaults = {
        "tokens": "16",
        "language": "java",
        "report_directory": "/bin/reports",
        "analysis_directory": "/bla/input",
    }

    # act
    settings = get_settings(args)

    # assert
    assert settings == expected_defaults


@patch("src.cpd.cpd_analysis.csv")
def test_that_profile_is_saved_correctly(csv_mock):
    """Test that the code duplication profile is save correctly."""

    # arrange
    metrics = {"duplicated_loc": 100, "total_loc": 200}

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow(["Duplicated Lines Of Code", "Total Lines Of Code"]),
        call.writerow([100, 200]),
    ]

    # act
    with patch("src.cpd.cpd_analysis.open", mock_open()) as mocked_file:
        save_duplication_profile("code_duplication.csv", metrics)
        mocked_file.assert_called_once_with("code_duplication.csv", "w", encoding="utf-8")

    # assert
    csv_mock.writer().writerow.assert_has_calls(calls)
    assert csv_mock.writer().writerow.call_count == 2
