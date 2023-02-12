"""Analyze the commit activity for test and production code."""

import datetime
import os

import pandas as pd
import plotly.graph_objects as go

from dateutil.rrule import rrule, SU, WEEKLY
from pydriller import Repository


def determine_begin_date_of_the_week(date):
    """Determine the date of the first day of the week closest to the provided date."""

    begin_date_of_the_week = date - datetime.timedelta(days=date.isoweekday() % 7)

    return begin_date_of_the_week


def commit_contains_test_code(commit):
    """Check if the commit touches test code."""

    modified_test_code = False
    for modified_file in commit.modified_files:
        if modified_file.new_path:
            if "test" in modified_file.new_path.lower():
                modified_test_code = True
    return modified_test_code


def commit_contains_production_code(commit):
    """Check if the commit touches production code."""

    modified_production_code = False
    for modified_file in commit.modified_files:
        if modified_file.new_path:
            if "test" not in modified_file.new_path.lower():
                modified_production_code = True
    return modified_production_code


def determine_commits_in_period(repository, start_date, end_date):
    """Determine the commits that are made in the period from start_date to end_date."""

    production_code_commit_count = 0
    test_code_commit_count = 0
    number_of_commits = 0
    for commit in Repository(repository, since=start_date, to=end_date).traverse_commits():
        if commit_contains_test_code(commit):
            test_code_commit_count = test_code_commit_count + 1
        if commit_contains_production_code(commit):
            production_code_commit_count = production_code_commit_count + 1
        number_of_commits = number_of_commits + 1
    return number_of_commits, production_code_commit_count, test_code_commit_count


def determine_commit_activity(repository, start_date, end_date):
    """Determine the commit activity for the specified repository and period and return a dataframe."""

    production_commit_count = []
    test_commit_count = []
    commit_count = []

    cumulative_production_commits = 0
    cumulative_test_commits = 0
    cumulative_commits = 0

    for date in rrule(freq=WEEKLY, wkst=SU, byweekday=SU, dtstart=start_date, until=end_date):
        one_week_later = date + datetime.timedelta(days=7)
        number_of_commits, production_commits, test_commits = determine_commits_in_period(
            repository, date, one_week_later
        )

        cumulative_commits = cumulative_commits + number_of_commits
        cumulative_production_commits = cumulative_production_commits + production_commits
        cumulative_test_commits = cumulative_test_commits + test_commits

        production_commit_count.append(cumulative_production_commits)
        test_commit_count.append(cumulative_test_commits)
        commit_count.append(number_of_commits)
        print(date, one_week_later, production_commits, test_commits, number_of_commits)

    dataframe = pd.DataFrame(
        {
            "date": list(rrule(freq=WEEKLY, wkst=SU, byweekday=SU, dtstart=start_date, until=end_date)),
            "production_commit_count": production_commit_count,
            "test_commit_count": test_commit_count,
            "commit_count": commit_count
        }
    )

    return dataframe


def save_test_activity(settings, dataframe):
    """Save the test activity to a csv file in the reports/metrics directory."""

    metrics_file = os.path.join(settings["report_directory"], "metrics", "test_activity.csv")
    dataframe.to_csv(metrics_file, sep=",", mode="w", columns=["date", "production_commit_count", "test_commit_count"])


def save_commit_activity(settings, dataframe):
    """Save the commit activity to a csv file in the report/metrics directory."""
    metrics_file = os.path.join(settings["report_directory"], "metrics", "commit_activity.csv")
    dataframe.to_csv(metrics_file, sep=",", mode="w", columns=["date", "commit_count"])


def show_commit_activity(dataframe):
    """Show the commit activity graph."""

    fig = go.Figure()
    fig.update_layout(title_text="Commit activity", yaxis_title="# Commits", xaxis_title="Date")
    fig.add_trace(
        go.Bar(
            name="Commit count",
            x=dataframe["date"],
            y=dataframe["commit_count"],
        )
    )
    fig.show()


def show_test_activity(dataframe):
    """Show the test activity graph."""

    fig2 = go.Figure()
    fig2.update_layout(title_text="Production vs. test activity", yaxis_title="# Commits", xaxis_title="Date")
    fig2.add_trace(
        go.Scatter(
            name="Production commit count",
            mode="markers+lines",
            x=dataframe["date"],
            y=dataframe["production_commit_count"],
        )
    )
    fig2.add_trace(
        go.Scatter(
            name="Test commit count",
            mode="markers+lines",
            x=dataframe["date"],
            y=dataframe["test_commit_count"],
        )
    )
    fig2.show()


def analyze_commits(settings):
    """Analyze the commits and return a dataframe containing the commits, production commits, test commits."""

    period_start = determine_begin_date_of_the_week(settings["period_start"])
    period_end = determine_begin_date_of_the_week(settings["period_end"])

    return determine_commit_activity(settings["repository"], period_start, period_end)
