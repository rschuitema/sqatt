"""Unit tests for the repository analysis functions."""
import datetime
from unittest.mock import patch

import pytest as pytest

from src.repositorymining.repository_analysis import parse_arguments, get_settings


class ChurnAnalysisMocks:
    """Collection of mocks for all analysis functions."""

    def __init__(self):
        """Create the analysis patches."""
        self.analyze_churn_complexity_patch = patch("src.repositorymining.repository_analysis.analyze_churn_complexity")
        self.analyze_churn_patch = patch("src.repositorymining.repository_analysis.analyze_file_churn")
        self.save_churn_complexity_patch = patch("src.repositorymining.repository_analysis.save_churn_complexity")
        self.show_churn_complexity_patch = patch("src.repositorymining.repository_analysis.show_churn_complexity_chart")

        self.analyze_churn_complexity_mock = None
        self.analyze_churn_mock = None
        self.save_churn_complexity_mock = None
        self.show_churn_complexity_mock = None

    def start(self):
        """Start the patches."""

        self.analyze_churn_complexity_mock = self.analyze_churn_complexity_patch.start()
        self.analyze_churn_mock = self.analyze_churn_patch.start()
        self.save_churn_complexity_mock = self.save_churn_complexity_patch.start()
        self.show_churn_complexity_mock = self.show_churn_complexity_patch.start()

    def stop(self):
        """Stop the patches."""
        self.analyze_churn_complexity_patch.stop()
        self.save_churn_complexity_patch.stop()
        self.save_churn_complexity_patch.stop()


@pytest.fixture
def churn_analysis_mocks():
    """Fixture for creating analysis mocks."""

    mocks = ChurnAnalysisMocks()
    mocks.start()
    yield mocks
    mocks.stop()


def test_option_churn_only_performs_churn_analysis(churn_analysis_mocks):
    """Test that option churn only analyzes the churn."""

    # arrange
    args = parse_arguments(["/bla/input", "--churn"])

    # act
    args.func(args)

    # assert
    churn_analysis_mocks.analyze_churn_mock.assert_called_once()


def test_option_churn_complexity_only_performs_churn_complexity_analysis(churn_analysis_mocks):
    """Test that option churncomplexity only analyzes the churn vs complexity."""

    # arrange
    args = parse_arguments(["/bla/input", "--churncomplexity"])

    # act
    args.func(args)

    # assert
    churn_analysis_mocks.analyze_churn_complexity_mock.assert_called_once()
    churn_analysis_mocks.save_churn_complexity_mock.assert_called_once()
    churn_analysis_mocks.show_churn_complexity_mock.assert_called_once()


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
