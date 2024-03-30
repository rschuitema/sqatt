"""Unit test for churn analysis."""

import os
from datetime import datetime
from unittest.mock import patch, Mock, call, mock_open, ANY

import pandas

from src.repositorymining.analyze_churn import (
    measure_file_complexity,
    measure_file_churn,
    save_file_churn,
    analyze_churn_complexity,
    show_churn_complexity_chart,
)


@patch("os.path.exists")
@patch("src.repositorymining.analyze_churn.Subprocess")
def test_measure_file_complexity_calls_lizard_with_correct_parameters(subprocess_mock, exists_mock):
    """Test that lizard is called with the correct parameters to measure file complexity."""

    # arrange
    settings = {
        "repository": "github/my_repository",
        "report_directory": "/report_root/reports",
        "period_start": datetime(year=2024, month=1, day=1),
        "period_end": datetime(year=2024, month=3, day=1),
        "period_frequency": "WEEKLY",
    }

    exists_mock.return_value = True

    # act
    measure_file_complexity(settings)

    # assert
    subprocess_mock.assert_called_with(
        [
            "lizard",
            "--xml",
            f'-o{os.path.join(settings["report_directory"], "function_metrics.xml")}',
            settings["repository"],
        ],
        verbose=3,
    )


@patch("src.repositorymining.analyze_churn.CodeChurn")
def test_measure_churn_returns_sorted_churn_per_file(code_churn_mock):
    """test that measure churn returns a sorted list of churn per file."""

    # arrange
    code_churn_mock.return_value.files = {"file1": [1, 2, 3], None: [1, 2], "file2": [4, 5, 6, 7]}

    settings = {
        "repository": "github/my_repository",
        "report_directory": "/report_root/reports",
        "period_start": datetime(year=2024, month=1, day=1),
        "period_end": datetime(year=2024, month=3, day=1),
        "period_frequency": "WEEKLY",
    }

    # act
    churn_per_file = measure_file_churn(settings)

    # assert
    assert len(churn_per_file) == 2
    assert churn_per_file[0] == (os.path.join("github/my_repository", "file2"), 22)
    assert churn_per_file[1] == (os.path.join("github/my_repository", "file1"), 6)


@patch("src.repositorymining.analyze_churn.csv")
def test_save_file_churn_saves_metrics_to_file(csv_mock):
    """Test that the churn is saved."""

    # arrange
    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow(["File", "Churn"]),
        call.writerow(["File1", 200]),
        call.writerow(["Unknown", 100]),
        call.writerow(["File2", 60]),
    ]

    report_dir = "bla/report"
    churn = [("File1", 200), (None, 100), ("File2", 60)]
    churn_report_file = os.path.join(report_dir, "churn.csv")

    # act
    with patch("src.repositorymining.analyze_churn.open", mock_open()) as mocked_file:
        save_file_churn(report_dir, churn)

        # assert
        mocked_file.assert_called_once_with(churn_report_file, "w", encoding="utf-8")
        csv_mock.writer().assert_has_calls(calls)


@patch("os.path.exists")
@patch("src.repositorymining.analyze_churn.measure_file_complexity")
@patch("src.repositorymining.analyze_churn.analyze_file_churn")
@patch("src.repositorymining.analyze_churn.pd.read_xml")
@patch("src.repositorymining.analyze_churn.pd.read_csv")
def test_analyze_churn_complexity(
    read_csv_mock, read_xml_mock, analyze_file_churn_mock, measure_file_complexity_mock, exists_mock
):
    """Test te analysis of the churn vs complexity."""

    # arrange
    settings = {
        "repository": "github/my_repository",
        "report_directory": "/report_root/reports",
        "period_start": datetime(year=2024, month=1, day=1),
        "period_end": datetime(year=2024, month=3, day=1),
        "period_frequency": "WEEKLY",
    }

    churn_data = pandas.DataFrame(
        {"File": pandas.Series(["File1", "File2", "File3"]), "Churn": pandas.Series([4, 5, 6])}
    )

    complexity_data = pandas.DataFrame(
        {
            "File": pandas.Series(["File1", "File2", "File3"]),
            "Nr": pandas.Series([1, 2, 3]),
            "NCSS": pandas.Series([12, 44, 23]),
            "CCN": pandas.Series([3, 12, 6]),
            "Functions": pandas.Series([5, 9, 16]),
        }
    )

    expected_data = pandas.DataFrame(
        {
            "File": pandas.Series(["File1", "File2", "File3"]),
            "NCSS": pandas.Series([12, 44, 23]),
            "CCN": pandas.Series([3, 12, 6]),
            "Functions": pandas.Series([5, 9, 16]),
            "Churn": pandas.Series([4, 5, 6]),
        }
    )

    read_csv_mock.return_value = churn_data
    read_xml_mock.return_value = complexity_data
    exists_mock.return_value = True

    # act
    with patch("src.repositorymining.analyze_churn.open", mock_open()):
        actual_data = analyze_churn_complexity(settings)

        # assert
        pandas.testing.assert_frame_equal(expected_data, actual_data)

        analyze_file_churn_mock.assert_called_once()
        measure_file_complexity_mock.assert_called_once()


@patch("src.repositorymining.analyze_churn.go.Figure")
def test_show_code_volume_profile_figure_created_with_correct_values(figure_mock):
    """Test that the figure is created with the correct values."""

    # arrange
    data_frame = pandas.DataFrame(
        {
            "File": pandas.Series(["File1", "File2", "File3"]),
            "NCSS": pandas.Series([12, 42, 23]),
            "CCN": pandas.Series([3, 12, 6]),
            "Functions": pandas.Series([5, 9, 16]),
            "Churn": pandas.Series([4, 5, 6]),
        }
    )

    # act
    with patch("src.profile.show.go.Scatter") as scatter_mock:
        figure_mock.show = Mock()
        show_churn_complexity_chart(data_frame)

    # assert
    scatter_mock.assert_called_once_with(
        x=data_frame["Churn"],
        y=data_frame["CCN"],
        text=data_frame["File"],
        hovertemplate=ANY,
        mode=ANY,
        marker=ANY,
    )

    figure_mock().update_layout.assert_called_once()
    figure_mock().show.assert_called_once()
