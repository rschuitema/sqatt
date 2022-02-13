"""Unit tests for the repository analysis functions."""
import datetime
from src.repositorymining.repository_analysis import parse_arguments, get_settings


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
