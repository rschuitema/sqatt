"""Unit test for cloc code size analysis."""
import os
from unittest.mock import patch, Mock, call, mock_open, ANY

from src.cloc.cloc_code_size import (
    calculate_test_code_to_production_code_ratio,
    calculate_comment_to_code_ratio,
    write_code_size_header,
    write_code_size_metrics,
    save_code_metrics,
    analyze_size_per_code_type,
    show_code_profile,
    show_code_type_profile,
)
from src.profile.colors import PROFILE_COLORS


def test_code_size_test_code_size_ratio_calculated_correctly():
    """Test that the code size to test code size ratio is calculated correctly."""

    production_code_metrics = {"SUM": {"code": 120, "comment": 30}}
    test_code_metrics = {"SUM": {"code": 30, "comment": 10}}

    ratio = calculate_test_code_to_production_code_ratio(production_code_metrics, test_code_metrics)

    assert ratio == 30 / 120


def test_comment_to_code_ratio_calculated_correctly():
    """Test that the comment to code ratio is calculated correctly."""

    production_code_metrics = {"SUM": {"code": 120, "comment": 30}}
    test_code_metrics = {"SUM": {"code": 30, "comment": 10}}
    ratio = calculate_comment_to_code_ratio(production_code_metrics, test_code_metrics)

    assert ratio == 40 / 150


@patch("src.cloc.cloc_code_size.csv")
def test_write_header(csv_mock):
    """Test that the correct header is written to the csv file."""

    csv_mock.writer = Mock(writerow=Mock())
    calls = [call.writerow(["Blank Lines", "Lines Of Code", "Comment Lines"])]
    write_code_size_header(csv_mock.writer)

    csv_mock.writer.writerow.assert_has_calls(calls)


@patch("src.cloc.cloc_code_size.csv")
def test_write_code_size_metrics(csv_mock):
    """Test that the correct metrics are written to the csv file."""

    metrics = {
        "Java": {"files": 201, "blank": 20, "code": 1003, "comment": 230},
        "C": {"files": 100, "blank": 7, "code": 1220, "comment": 30},
        "SUM": {"files": 301, "blank": 7, "code": 2120, "comment": 130},
    }

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow([7, 2120, 130]),
    ]
    write_code_size_metrics(csv_mock.writer, metrics)

    csv_mock.writer.writerow.assert_has_calls(calls)


@patch("src.cloc.cloc_code_size.csv")
def test_save_metrics(csv_mock):
    """Test that the metrics are saved."""

    production_code_size_file = "code_size.csv"

    production_code_metrics = {
        "Java": {"files": 201, "blank": 20, "code": 1003, "comment": 230},
        "C#": {"files": 100, "blank": 7, "code": 1220, "comment": 30},
        "SUM": {"files": 301, "blank": 7, "code": 2120, "comment": 130},
    }

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow(["Blank Lines", "Lines Of Code", "Comment Lines"]),
        call.writerow([7, 2120, 130]),
    ]
    with patch("src.cloc.cloc_code_size.open", mock_open()) as mocked_file:
        save_code_metrics(production_code_size_file, production_code_metrics)

        mocked_file.assert_called_once_with(production_code_size_file, "w", encoding="utf-8")
        csv_mock.writer().assert_has_calls(calls)


@patch("src.cloc.cloc_code_size.save_code_type_profile")
@patch("src.cloc.cloc_code_size.create_report_directory")
def test_metrics_are_empty_when_no_code_type_specified(create_report_directory_mock, save_code_type_profile_mock):
    """Test that the metrics are empty when no code type is specified."""

    # arrange
    settings = {"report_directory": "./reports/not_exists", "code_type": ""}

    create_report_directory_mock.return_value = settings["report_directory"]

    # act
    metrics = analyze_size_per_code_type(settings)

    # assert
    assert bool(metrics) is False
    save_code_type_profile_mock.assert_called_once()


@patch("src.cloc.cloc_code_size.save_code_type_profile")
@patch("src.cloc.cloc_code_size.save_code_metrics")
@patch("src.cloc.cloc_code_size.get_size_metrics")
@patch("src.cloc.cloc_code_size.measure_lines_of_code")
@patch("src.reporting.reporting.create_report_directory")
def test_analyze_size_correct_metrics_per_code_type_are_saved_to_report_file(
    create_report_directory_mock,
    measure_loc_mock,
    get_size_metrics_mock,
    save_code_metrics_mock,
    save_code_type_profile_mock,
):
    """Test that the correct metrics per code type are saved to the report file."""

    # arrange
    settings = {
        "report_directory": "./reports",
        "code_type": ["production"],
        "analysis_directory": "src",
        "production_filter": "filter1",
        "test_filter": "filter2",
    }

    create_report_directory_mock.return_value = settings["report_directory"]
    get_size_metrics_mock.return_value = 100

    # act
    metrics = analyze_size_per_code_type(settings)

    # assert
    report_file_name = os.path.join("./reports", "production_code_volume_profile.csv")
    measure_loc_mock.assert_called_once_with("src", report_file_name, "filter1")
    get_size_metrics_mock.assert_called_once_with(report_file_name)
    save_code_metrics_mock.assert_called_once_with(report_file_name, 100)
    save_code_type_profile_mock.assert_called_once_with(settings["report_directory"], {"production": 100})

    assert metrics["production"] == 100


@patch("src.profile.show.go.Figure")
def test_show_code_type_profile_figure_created_with_correct_values(figure_mock):
    """Test that the figure is created with the correct values."""

    # arrange
    metrics = {
        "production": {
            "SUM": {"files": "70", "blank": "879", "comment": "395", "code": "3072"},
            "Python": {"files": "54", "blank": "843", "comment": "391", "code": "1889"},
        },
        "test": {
            "SUM": {"files": "17", "blank": "766", "comment": "568", "code": "1652"},
            "Python": {"files": "16", "blank": "763", "comment": "568", "code": "1647"},
        },
        "third_party": {
            "SUM": {"files": "10", "blank": "172", "comment": "67", "code": "598"},
            "Python": {"files": "5", "blank": "134", "comment": "67", "code": "373"},
        },
        "generated": {
            "SUM": {"files": "4", "blank": "85", "comment": "47", "code": "1597"},
            "Python": {"files": "2", "blank": "85", "comment": "46", "code": "127"},
        },
    }

    # act
    with patch("src.profile.show.go.Pie") as pie_mock:
        figure_mock.show = Mock()
        show_code_type_profile(metrics)

    # assert
    pie_mock.assert_called_once_with(
        title={"text": "Code type breakdown"},
        labels=["Production", "Test", "Third Party", "Generated"],
        values=["3072", "1652", "598", "1597"],
        hole=ANY,
        marker_colors=PROFILE_COLORS,
        marker_line=ANY,
    )

    figure_mock().show.assert_called_once()


@patch("src.profile.show.go.Figure")
def test_show_code_profile_figure_created_with_correct_values(figure_mock):
    """Test that the code type figure is created with the correct values."""

    # arrange
    code_profile = {
        "SUM": {"files": 70, "blank": 879, "code": 3061, "comment": 395},
        "C#": {"files": 100, "blank": 7, "code": 1220, "comment": 30},
    }

    # act
    with patch("src.profile.show.go.Pie") as pie_mock:
        figure_mock.show = Mock()
        show_code_profile(code_profile, "Production")

    # assert
    pie_mock.assert_called_once_with(
        title={"text": "Production code <br> breakdown"},
        labels=["Blank Lines", "Lines of Code", "Comment Lines"],
        values=[879, 3061, 395],
        hole=ANY,
        marker_colors=PROFILE_COLORS,
        marker_line=ANY,
    )

    figure_mock().show.assert_called_once()
