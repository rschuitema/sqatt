"""Unit test for churn analysis."""

import os
from datetime import datetime
from unittest.mock import patch, Mock, call, mock_open

from src.repositorymining.analyze_churn import measure_file_complexity, measure_file_churn, save_file_churn


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
