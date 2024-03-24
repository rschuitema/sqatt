"""Unit tests for the repository analysis functions."""

import datetime
from unittest.mock import patch

import pytest

from src.repositorymining.repository_analysis import parse_arguments, get_settings


class RepositoryAnalysisMocks:
    """Collection of mocks for all analysis functions."""

    def __init__(self):
        """Create the analysis patches."""

        self.analyze_churn_patch = patch("src.repositorymining.repository_analysis.analyze_file_churn")

        self.analyze_churn_complexity_patch = patch("src.repositorymining.repository_analysis.analyze_churn_complexity")
        self.save_churn_complexity_patch = patch("src.repositorymining.repository_analysis.save_churn_complexity")
        self.show_churn_complexity_patch = patch("src.repositorymining.repository_analysis.show_churn_complexity_chart")

        self.analyze_commits_patch = patch("src.repositorymining.repository_analysis.analyze_commits")
        self.save_test_activity_patch = patch("src.repositorymining.repository_analysis.save_test_activity")
        self.show_test_activity_patch = patch("src.repositorymining.repository_analysis.show_test_activity")

        self.save_commit_activity_patch = patch("src.repositorymining.repository_analysis.save_commit_activity")
        self.show_commit_activity_patch = patch("src.repositorymining.repository_analysis.show_commit_activity")

        self.analyze_churn_mock = None

        self.analyze_churn_complexity_mock = None
        self.save_churn_complexity_mock = None
        self.show_churn_complexity_mock = None

        self.analyze_commits_mock = None
        self.save_test_activity_mock = None
        self.show_test_activity_mock = None

        self.save_commit_activity_mock = None
        self.show_commit_activity_mock = None

    def start(self):
        """Start the patches."""

        self.analyze_churn_mock = self.analyze_churn_patch.start()

        self.analyze_churn_complexity_mock = self.analyze_churn_complexity_patch.start()
        self.save_churn_complexity_mock = self.save_churn_complexity_patch.start()
        self.show_churn_complexity_mock = self.show_churn_complexity_patch.start()

        self.analyze_commits_mock = self.analyze_commits_patch.start()
        self.save_test_activity_mock = self.save_test_activity_patch.start()
        self.show_test_activity_mock = self.show_test_activity_patch.start()

        self.save_commit_activity_mock = self.save_commit_activity_patch.start()
        self.show_commit_activity_mock = self.show_commit_activity_patch.start()

    def stop(self):
        """Stop the patches."""

        self.analyze_churn_patch.stop()

        self.analyze_churn_complexity_patch.stop()
        self.save_churn_complexity_patch.stop()
        self.show_churn_complexity_patch.stop()

        self.analyze_commits_patch.stop()
        self.save_test_activity_patch.stop()
        self.show_test_activity_patch.stop()

        self.save_commit_activity_patch.stop()
        self.show_commit_activity_patch.stop()


@pytest.fixture  # pylint disable=W0621
def repository_analysis_mocks():
    """Fixture for creating analysis mocks."""

    mocks = RepositoryAnalysisMocks()
    mocks.start()
    yield mocks
    mocks.stop()


def test_option_churn_only_performs_churn_analysis(repository_analysis_mocks):
    """Test that option churn only analyzes the churn."""

    # arrange
    args = parse_arguments(["/bla/input", "--churn"])

    # act
    args.func(args)

    # assert
    repository_analysis_mocks.analyze_churn_mock.assert_called_once()


def test_option_churn_complexity_only_performs_churn_complexity_analysis(repository_analysis_mocks):
    """Test that option churncomplexity only analyzes the churn vs complexity."""

    # arrange
    args = parse_arguments(["/bla/input", "--churncomplexity"])

    # act
    args.func(args)

    # assert
    repository_analysis_mocks.analyze_churn_complexity_mock.assert_called_once()
    repository_analysis_mocks.save_churn_complexity_mock.assert_called_once()
    repository_analysis_mocks.show_churn_complexity_mock.assert_called_once()


def test_option_test_activity_only_performs_test_activity_analysis(repository_analysis_mocks):
    """Test that option test-activity only analyzes the test activity."""

    # arrange
    args = parse_arguments(["/bla/input", "--test-activity"])

    # act
    args.func(args)

    # assert
    repository_analysis_mocks.analyze_commits_mock.assert_called_once()
    repository_analysis_mocks.save_test_activity_mock.assert_called_once()
    repository_analysis_mocks.show_test_activity_mock.assert_called_once()


def test_option_commits_only_performs_commit_activity_analysis(repository_analysis_mocks):
    """Test that option commits only analyzes the commit activity."""

    # arrange
    args = parse_arguments(["/bla/input", "--commits"])

    # act
    args.func(args)

    # assert
    repository_analysis_mocks.analyze_commits_mock.assert_called_once()
    repository_analysis_mocks.save_commit_activity_mock.assert_called_once()
    repository_analysis_mocks.show_commit_activity_mock.assert_called_once()


def test_option_all_performs_all_analysis(repository_analysis_mocks):
    """Test that option all performs all analyzes."""

    # arrange
    args = parse_arguments(["/bla/input", "--all"])

    # act
    args.func(args)

    # assert
    repository_analysis_mocks.analyze_commits_mock.assert_called_once()
    repository_analysis_mocks.save_commit_activity_mock.assert_called_once()
    repository_analysis_mocks.show_commit_activity_mock.assert_called_once()

    repository_analysis_mocks.save_test_activity_mock.assert_called_once()
    repository_analysis_mocks.show_test_activity_mock.assert_called_once()

    repository_analysis_mocks.analyze_churn_complexity_mock.assert_called_once()
    repository_analysis_mocks.save_churn_complexity_mock.assert_called_once()
    repository_analysis_mocks.show_churn_complexity_mock.assert_called_once()

    repository_analysis_mocks.analyze_churn_mock.assert_called_once()


def test_default_value_for_end_date_is_today():
    """Test that when the --end-date option is not provided the end date is today."""

    # arrange
    args = parse_arguments(["/bla/input", "--commit"])

    # act
    settings = get_settings(args)

    # assert
    assert datetime.datetime.today().day == settings["period_end"].day
    assert datetime.datetime.today().month == settings["period_end"].month
    assert datetime.datetime.today().year == settings["period_end"].year


def test_default_value_for_start_date_is_one_year_ago():
    """Test that when the --start-date option is not provided the start date is one year ago."""

    # arrange
    args = parse_arguments(["/bla/input", "--commit"])

    # act
    settings = get_settings(args)

    # assert
    one_year_ago = datetime.datetime.today() - datetime.timedelta(days=365)
    assert one_year_ago.day == settings["period_start"].day
    assert one_year_ago.month == settings["period_start"].month
    assert one_year_ago.year == settings["period_start"].year


def test_default_value_for_frequency_is_weekly():
    """Test that when the --end-date option is not provided the start date is one year ago."""

    # arrange
    args = parse_arguments(["/bla/input", "--commit"])

    # act
    settings = get_settings(args)

    # assert
    assert "WEEKLY" == settings["period_frequency"]
