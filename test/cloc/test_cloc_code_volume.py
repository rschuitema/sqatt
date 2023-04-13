"""Unit tests for the cloc code volume analysis."""
import csv
import os
from io import StringIO
from unittest.mock import patch, Mock, call, ANY, mock_open

from src.cloc.cloc_code_volume import (
    show_code_volume_profile,
    save_code_volume_profile,
    determine_total_code_volume,
    read_code_volume,
    calculate_test_code_to_production_code_ratio,
    calculate_comment_to_code_ratio,
    save_code_ratios,
    analyze_code_volume,
)
from src.profile.colors import PROFILE_COLORS


@patch("src.profile.show.go.Figure")
def test_show_code_volume_profile_figure_created_with_correct_values(figure_mock):
    """Test that the figure is created with the correct values."""

    # arrange
    metrics = {
        "Blank Lines": 100,
        "Lines Of Code": 200,
        "Comment Lines": 300,
    }

    # act
    with patch("src.profile.show.go.Pie") as pie_mock:
        figure_mock.show = Mock()
        show_code_volume_profile(metrics)

    # assert
    pie_mock.assert_called_once_with(
        title={"text": "Code volume breakdown"},
        labels=["Blank Lines", "Lines Of Code", "Comment Lines"],
        values=[100, 200, 300],
        hole=ANY,
        marker_colors=PROFILE_COLORS,
        marker_line=ANY,
    )

    figure_mock().show.assert_called_once()


@patch("src.cloc.cloc_code_volume.csv")
def test_save_code_volume_profile(csv_mock):
    """Test that the metrics are saved."""

    # arrange
    code_volume_profile = "code_volume_profile.csv"
    code_volume_profile_file = os.path.join("/bla/reports", "profiles", code_volume_profile)

    metrics = {
        "Blank Lines": 100,
        "Lines Of Code": 200,
        "Comment Lines": 300,
    }

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow(["Blank Lines", "Lines Of Code", "Comment Lines"]),
        call.writerow([100, 200, 300]),
    ]

    # act
    with patch("src.cloc.cloc_code_volume.open", mock_open()) as mocked_file:
        save_code_volume_profile("/bla/reports", metrics)

        # assert
        mocked_file.assert_called_once_with(code_volume_profile_file, "w", encoding="utf-8")
        csv_mock.writer().assert_has_calls(calls)


def test_that_determine_total_code_volume_calculates_correct_totals():
    """Test that the correct totals are calculated."""

    # arrange
    settings = {"code_type": ["production", "test", "generated"]}
    code_volume = {
        "production": {"Blank Lines": 10, "Lines Of Code": 300, "Comment Lines": 10},
        "test": {"Blank Lines": 20, "Lines Of Code": 200, "Comment Lines": 20},
        "generated": {"Blank Lines": 30, "Lines Of Code": 400, "Comment Lines": 30},
    }

    # act
    total_volume = determine_total_code_volume(settings, code_volume)

    # assert
    assert total_volume["Blank Lines"] == 60
    assert total_volume["Lines Of Code"] == 900
    assert total_volume["Comment Lines"] == 60


def test_that_totals_are_0_when_no_code_type_specified():
    """Test that the totals are 0 when no code type is specified."""

    # arrange
    settings = {"code_type": []}
    code_volume = {
        "production": {"Blank Lines": 20, "Lines Of Code": 300, "Comment Lines": 10},
        "test": {"Blank Lines": 20, "Lines Of Code": 200, "Comment Lines": 20},
        "generated": {"Blank Lines": 20, "Lines Of Code": 400, "Comment Lines": 30},
    }

    # act
    total_volume = determine_total_code_volume(settings, code_volume)

    # assert
    assert total_volume["Blank Lines"] == 0
    assert total_volume["Lines Of Code"] == 0
    assert total_volume["Comment Lines"] == 0


def test_read_code_volume_reads_correct_values():
    """Test that correct values are read."""

    # arrange
    report_file = "bla.csv"

    data = StringIO(
        """Blank Lines, Lines Of Code, Comment Lines
        10, 11, 12"""
    )

    test_reader = csv.DictReader(data, delimiter=",", skipinitialspace=True)

    # act
    with patch("src.cloc.cloc_code_volume.open", mock_open()) as mocked_file:
        code_volume = read_code_volume(report_file, test_reader)

    # assert
    mocked_file.assert_called_once_with(report_file, "r", newline="\n", encoding="utf-8")
    assert code_volume["Blank Lines"] == 10
    assert code_volume["Lines Of Code"] == 11
    assert code_volume["Comment Lines"] == 12


def test_code_size_test_code_size_ratio_calculated_correctly():
    """Test that the code size to test code size ratio is calculated correctly."""

    # arrange
    production_code_metrics = {
        "Blank Lines": 100,
        "Lines Of Code": 400,
        "Comment Lines": 300,
    }

    test_code_metrics = {
        "Blank Lines": 100,
        "Lines Of Code": 220,
        "Comment Lines": 300,
    }

    # act
    ratio = calculate_test_code_to_production_code_ratio(production_code_metrics, test_code_metrics)

    # assert
    assert ratio == 220 / 400


def test_comment_to_code_ratio_calculated_correctly():
    """Test that the comment to code ratio is calculated correctly."""

    # arrange
    code_metrics = {
        "Blank Lines": 100,
        "Lines Of Code": 600,
        "Comment Lines": 300,
    }

    # act
    ratio = calculate_comment_to_code_ratio(code_metrics)

    # assert
    assert ratio == 300 / 900


@patch("src.cloc.cloc_code_volume.csv")
def test_code_ratios_are_saved_correctly(csv_mock):
    """Test that the code ratio metrics are saved."""

    # arrange
    report_dir = "/bla/reports"
    code_ratio_file = os.path.join(report_dir, "profiles", "code_volume_ratios.csv")
    settings = {"report_directory": report_dir}

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow(["Comment To Code Ratio", "Test Code To Production Code Ratio"]),
        call.writerow([0.2, 0.321]),
    ]

    # act
    with patch("src.cloc.cloc_code_volume.open", mock_open()) as mocked_file:
        save_code_ratios(settings, 0.2, 0.321)

        # assert
        mocked_file.assert_called_once_with(code_ratio_file, "w", encoding="utf-8")
        csv_mock.writer().assert_has_calls(calls)


@patch("src.cloc.cloc_code_volume.save_code_ratios")
@patch("src.cloc.cloc_code_volume.show_code_volume_profile")
@patch("src.cloc.cloc_code_volume.save_code_volume_profile")
@patch("src.cloc.cloc_code_volume.read_code_volume")
def test_that_report_is_generated_in_correct_directory(read_mock, save_mock, show_mock, save_ratio_mock):
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

    code_volume = {"Blank Lines": 100, "Lines Of Code": 300, "Comment Lines": 200}
    read_mock.return_value = code_volume

    # act
    analyze_code_volume(settings)

    # assert
    assert save_mock.call_count == 1
    assert show_mock.call_count == 1
    assert save_ratio_mock.call_count == 1
