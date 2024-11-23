"""Unit test for the churn analysis."""

import os
from unittest.mock import patch, Mock, call, mock_open

from src.churn.churn import calculate_churn, remove_empty_lines, save_churn, parse_arguments, get_settings


def test_churn_calculation():
    """Test if the churn is calulated correctly."""

    git_log = os.linesep.join(
        [
            "test/test_lizard_analysis.py",
            "test/test_lizard_analysis.py",
            "test/test_lizard_analysis.py",
            "test/repositorymining/test_analye_churn.py",
            "test/repositorymining/test_analye_churn.py",
            "src/profile/sqatt_profiles.py",
        ]
    )

    churn = calculate_churn(git_log)

    expected_churn = [
        ("test/test_lizard_analysis.py", 3),
        ("test/repositorymining/test_analye_churn.py", 2),
        ("src/profile/sqatt_profiles.py", 1),
    ]
    assert churn == expected_churn


def test_remove_empty_lines():
    """Test if empty lines are removed."""

    git_log = """
test/repositorymining/test_analye_churn.py
test/repositorymining/test_analye_churn.py

test/repositorymining/test_analye_churn.py
test/test_lizard_analysis.py

test/test_lizard_analysis.py

"""

    log = remove_empty_lines(git_log)

    expected_log = os.linesep.join(
        [
            "test/repositorymining/test_analye_churn.py",
            "test/repositorymining/test_analye_churn.py",
            "test/repositorymining/test_analye_churn.py",
            "test/test_lizard_analysis.py",
            "test/test_lizard_analysis.py",
        ]
    )
    assert log == expected_log


@patch("src.churn.churn.csv")
def test_save_churn(csv_mock):
    """Test if the churn is saved correctly."""

    churn = [
        ("test/test_lizard_analysis.py", 3),
        ("test/repositorymining/test_analye_churn.py", 2),
        ("src/profile/sqatt_profiles.py", 1),
    ]

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow(["File", "Churn"]),
        call.writerow(["test/test_lizard_analysis.py", 3]),
        call.writerow(["test/repositorymining/test_analye_churn.py", 2]),
        call.writerow(["src/profile/sqatt_profiles.py", 1]),
    ]
    report_directory = "reports"

    churn_file = os.path.join("reports", "churn", "churn.csv")
    with patch("src.churn.churn.open", mock_open()) as mocked_file:
        save_churn(churn, report_directory)

        mocked_file.assert_called_once_with(churn_file, "w", encoding="utf8", newline="")
        csv_mock.writer().assert_has_calls(calls)


def test_get_settings():
    """Test if the correct settings are determined form the command line arguments."""

    args = parse_arguments(["/bla/input", "--output", "bla/reports", "--since", "1-1-2021"])

    settings = get_settings(args)

    expected_settings = {"repository": "/bla/input", "report_directory": "bla/reports", "since": "1-1-2021"}

    assert settings == expected_settings
