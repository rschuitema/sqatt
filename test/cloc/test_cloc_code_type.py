"""Unit tests for the cloc code type analysis."""

import os
from unittest.mock import patch, Mock, call, ANY, mock_open

import pytest

from src.cloc.cloc_code_type import (
    show_code_type_profile,
    save_code_type_profile,
    analyze_code_type,
    save_code_metrics,
    analyze_code_volume_per_code_type,
)
from src.profile.colors import PROFILE_COLORS


@patch("src.profile.show.go.Figure")
def test_show_code_type_profile_figure_created_with_correct_values(figure_mock):
    """Test that the figure is created with the correct values."""

    # arrange
    metrics = {
        "Production": {
            "SUM": {"files": "70", "blank": "879", "comment": "395", "code": "3072"},
            "Python": {"files": "54", "blank": "843", "comment": "391", "code": "1889"},
        },
        "Test": {
            "SUM": {"files": "17", "blank": "766", "comment": "568", "code": "1652"},
            "Python": {"files": "16", "blank": "763", "comment": "568", "code": "1647"},
        },
        "Third Party": {
            "SUM": {"files": "10", "blank": "172", "comment": "67", "code": "598"},
            "Python": {"files": "5", "blank": "134", "comment": "67", "code": "373"},
        },
        "Generated": {
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


TEST_DATA = [
    {"production": {"SUM": {}}, "test": {"SUM": {}}, "generated": {"SUM": {}}, "third_party": {"SUM": {}}},
    {"production": {"SUM": {}}, "test": {"SUM": {}}, "generated": {"SUM": {}}},
    {"production": {"SUM": {}}, "test": {"SUM": {}}},
    {"production": {"SUM": {}}},
]


@pytest.mark.parametrize("metrics", TEST_DATA)
@patch("src.cloc.cloc_code_type.csv")
def test_save_code_type_profile_saves_configured_metrics(csv_mock, metrics):
    """Test that the metrics are saved that are configured in the config file."""

    # arrange
    code_type_profile = "code_type_profile.csv"
    code_type_profile_file = os.path.join("/bla/reports", code_type_profile)

    lines_of_code = 100
    header = []
    values = []
    for metric in metrics:
        metrics[metric]["SUM"]["code"] = lines_of_code
        header.append(metric)
        values.append(lines_of_code)
        lines_of_code = lines_of_code + 100

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow(header),
        call.writerow(values),
    ]

    # act
    with patch("src.cloc.cloc_code_type.open", mock_open()) as mocked_file:
        save_code_type_profile("/bla/reports", metrics)

        # assert
        mocked_file.assert_called_once_with(code_type_profile_file, "w", encoding="utf-8")
        csv_mock.writer().assert_has_calls(calls)


@patch("src.cloc.cloc_code_type.csv")
def test_save_code_metrics(csv_mock):
    """Test that the metrics are saved."""

    # arrange
    code_size_profile = os.path.join("/bla/reports", "code_size_profile.csv")

    metrics = {
        "Java": {"files": 201, "blank": 1, "code": 100, "comment": 10},
        "C": {"files": 100, "blank": 2, "code": 200, "comment": 20},
        "SUM": {"files": 301, "blank": 3, "code": 300, "comment": 30},
    }

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow(["Blank Lines", "Lines Of Code", "Comment Lines"]),
        call.writerow([3, 300, 30]),
    ]

    # act
    with patch("src.cloc.cloc_code_type.open", mock_open()) as mocked_file:
        save_code_metrics(code_size_profile, metrics)

        # assert
        mocked_file.assert_called_once_with(code_size_profile, "w", encoding="utf-8")
        csv_mock.writer().assert_has_calls(calls)


@patch("src.cloc.cloc_code_type.show_code_type_profile")
@patch("src.cloc.cloc_code_type.save_code_type_profile")
@patch("src.cloc.cloc_code_type.analyze_code_volume_per_code_type")
@patch("src.cloc.cloc_code_type.create_report_directory")
def test_that_report_is_generated_in_correct_directory(report_mock, volume_mock, save_mock, show_mock):
    """Test that the report is saved in the correct directory."""

    # arrange
    settings = {
        "analysis_directory": "/bla/input",
        "code_type": ["production", "test"],
        "production_filter": "--exclude-dir=test,tst",
        "test_filter": "--match-d=(test|tst)",
        "file_size_filter": "--exclude-dir=test,tst",
        "report_directory": "/bla/reports",
    }

    report_directory = os.path.join("/bla/reports", "profiles")
    report_mock.return_value = report_directory
    # act
    analyze_code_type(settings)

    # assert
    report_mock.assert_called_once_with(report_directory)
    assert volume_mock.call_count == 2
    assert save_mock.call_count == 1
    assert show_mock.call_count == 1


@patch("src.cloc.cloc_code_type.show_code_type_profile")
@patch("src.cloc.cloc_code_type.save_code_type_profile")
@patch("src.cloc.cloc_code_type.analyze_code_volume_per_code_type")
@patch("src.cloc.cloc_code_type.create_report_directory")
def test_that_metrics_are_empty_when_no_code_type_specified(report_mock, volume_mock, save_mock, show_mock):
    """Test that the report is saved in the correct directory."""

    # arrange
    settings = {
        "analysis_directory": "/bla/input",
        "code_type": [],
        "production_filter": "--exclude-dir=test,tst",
        "test_filter": "--match-d=(test|tst)",
        "file_size_filter": "--exclude-dir=test,tst",
        "report_directory": "/bla/reports",
    }

    report_directory = os.path.join("/bla/reports", "profiles")
    report_mock.return_value = report_directory

    # act
    analyze_code_type(settings)

    # assert
    report_mock.assert_called_once_with(report_directory)
    volume_mock.assert_not_called()
    save_mock.assert_called_once_with(report_directory, {})
    show_mock.assert_called_once_with({})


@patch("src.cloc.cloc_code_type.save_code_metrics")
@patch("src.cloc.cloc_code_type.get_size_metrics")
@patch("src.cloc.cloc_code_type.measure_lines_of_code")
@patch("src.cloc.cloc_code_type.create_report_directory")
def test_that_correct_lines_of_code_are_measured_for_code_type(report_mock, measure_mock, size_mock, save_mock):
    """Test that the correct lines of code are measured for the specified code type."""

    # arrange
    settings = {
        "analysis_directory": "/bla/input",
        "code_type": ["production"],
        "production_filter": "--exclude-dir=test,tst",
        "test_filter": "--match-d=(test|tst)",
        "file_size_filter": "--exclude-dir=test,tst",
        "report_directory": "/bla/reports",
    }

    report_directory = "/bla/reports"
    report_file = os.path.join(report_directory, "metrics", "production_code_volume_profile.csv")
    report_mock.return_value = report_directory
    size_mock.return_value = {}

    # act
    analyze_code_volume_per_code_type(settings, "production")

    # assert
    report_mock.assert_called_once_with(report_directory)
    measure_mock.assert_called_once_with(settings["analysis_directory"], report_file, settings["production_filter"])
    size_mock.assert_called_once_with(report_file)
    save_mock.assert_called_once_with(report_file, {})
