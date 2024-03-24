"""Unit test for cloc file size analysis."""

import csv
import os
from io import StringIO
from unittest.mock import patch, Mock, call, mock_open

from src.cloc.cloc_analyze_file_size import (
    save_file_size_metrics,
    determine_profile,
    get_file_size_metrics,
    measure_file_size,
    analyze_file_size,
)
from src.profile.sqatt_profiles import create_file_size_profile


@patch("src.cloc.cloc_analyze_file_size.csv")
@patch("src.cloc.cloc_analyze_file_size.create_report_directory")
def test_that_metrics_are_saved_to_file_size_metrics_csv_in_metric_directory(create_report_directory_mock, csv_mock):
    """Test that the metrics are saved."""

    report_dir = os.path.join("bla", "metrics")
    create_report_directory_mock.return_value = report_dir

    file_size_metrics = {
        "File1": {"language": "Java", "blank": 20, "code": 1003, "comment": 230},
        "File2": {"language": "C++", "blank": 7, "code": 1220, "comment": 30},
        "File3": {"language": "Python", "blank": 7, "code": 2120, "comment": 130},
    }

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow(["Filename", "Language", "Blank Lines", "Lines of Code", "Comment Lines"]),
        call.writerow(["File1", "Java", 20, 1003, 230]),
        call.writerow(["File2", "C++", 7, 1220, 30]),
        call.writerow(["File3", "Python", 7, 2120, 130]),
    ]
    with patch("src.cloc.cloc_analyze_file_size.open", mock_open()) as mocked_file:
        save_file_size_metrics(file_size_metrics, report_dir)

        mocked_file.assert_called_once_with(report_dir, "w", encoding="utf-8")
        csv_mock.writer().assert_has_calls(calls)


def test_that_file_size_profile_is_determined_correctly():
    """Test that file size profile is determined correctly."""

    file_size_metrics = {
        "File1": {"language": "Java", "blank": 20, "code": 50, "comment": 230},
        "File2": {"language": "C++", "blank": 20, "code": 200, "comment": 30},
        "File3": {"language": "Python", "blank": 20, "code": 600, "comment": 20},
        "File4": {"language": "C", "blank": 20, "code": 2000, "comment": 50},
        "File5": {"language": "Python", "blank": 20, "code": 200, "comment": 10},
    }

    profile = determine_profile(file_size_metrics)

    assert profile.name() == "File size"
    assert profile.total_loc() == 3050
    assert profile.regions()[0].loc() == 50
    assert profile.regions()[1].loc() == 400
    assert profile.regions()[2].loc() == 600
    assert profile.regions()[3].loc() == 2000


def test_that_metrics_that_have_no_filename_are_not_collected():
    """Test that metrics that have no filename are not collected."""

    report_file = "bla.csv"

    data = StringIO(
        """"filename","language","blank","code","comment"
           "File1", "python", 3,1,162
           "File2", "java", 24,12,124
           "", "c++", 24,12,50"""
    )

    test_reader = csv.DictReader(data, delimiter=",", skipinitialspace=True)
    with patch("src.cloc.cloc_analyze_file_size.open", mock_open()) as mocked_file:
        metrics = get_file_size_metrics(report_file, test_reader)

    # assert
    mocked_file.assert_called_once_with(report_file, "r", newline="\n", encoding="utf-8")
    assert len(metrics) == 2
    assert metrics["File1"]["language"] == "python"
    assert metrics["File2"]["language"] == "java"
    assert metrics["File2"]["comment"] == "124"


@patch("src.cloc.cloc_analyze_file_size.Subprocess")
def test_measure_file_size_calls_cloc_with_correct_parameters(subprocess_mock):
    """Test that cloc is called with the correct parameters to measure the file size."""

    # arrange
    input_dir = "/test_root/test_dir"
    report_file = "my_report"
    measure_filter = "my_filter"

    # act
    measure_file_size(input_dir, report_file, measure_filter)

    # assert
    subprocess_mock.assert_called_with(
        [
            "cloc",
            "--by-file",
            "--csv",
            "--csv-delimiter=,",
            "--hide-rate",
            f"--report-file={report_file}",
            measure_filter,
            input_dir,
        ],
        verbose=1,
    )


@patch("src.cloc.cloc_analyze_file_size.show_profile")
@patch("src.cloc.cloc_analyze_file_size.determine_profile")
@patch("src.cloc.cloc_analyze_file_size.save_file_size_metrics")
@patch("src.cloc.cloc_analyze_file_size.get_file_size_metrics")
@patch("src.cloc.cloc_analyze_file_size.measure_file_size")
@patch("src.cloc.cloc_analyze_file_size.create_report_directory")
def test_that_report_is_generated_in_correct_directory(
    report_mock, measure_mock, size_mock, save_mock, determine_mock, show_mock
):
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

    profiles_directory = os.path.join("/bla/reports", "profiles")
    metrics_directory = os.path.join("/bla/reports", "metrics")
    report_mock.side_effect = [metrics_directory, profiles_directory]

    size_mock.return_value = {}
    profile_mock = Mock(create_file_size_profile())
    determine_mock.return_value = profile_mock

    calls = [
        call.create_report_directory(metrics_directory),
        call.create_report_directory(profiles_directory),
    ]
    # act
    analyze_file_size(settings)

    # assert
    report_mock.has_calls(calls)
    assert measure_mock.call_count == 1
    assert size_mock.call_count == 1
    save_mock.assert_called_once_with({}, os.path.join(metrics_directory, "file_size_metrics.csv"))
    determine_mock.assert_called_once_with({})
    assert show_mock.call_count == 1
    assert len(profile_mock.method_calls) == 1
