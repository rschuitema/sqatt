"""
Functionality for analyzing repositories.

Code that resides in a test directory is considered test code.
The rest is considered production code.
"""

import argparse
import datetime
import sys

from src.repositorymining.analyze_churn import (
    analyze_file_churn,
    analyze_churn_complexity,
    save_churn_complexity,
    show_churn_complexity_chart,
)
from src.repositorymining.analyze_commit_activity import (
    analyze_commits,
    show_commit_activity,
    show_test_activity,
    save_commit_activity,
    save_test_activity,
)


def get_settings(args):
    """Determine the settings from the arguments that are passed on the command line."""

    settings = {
        "repository": args.repository,
        "report_directory": args.output,
        "period_start": args.start_date,
        "period_end": args.end_date,
        "period_frequency": args.frequency,
    }

    return settings


def perform_analysis(args):
    """Perform the requested analysis."""

    settings = get_settings(args)

    if args.all:
        dataframe = analyze_commits(settings)
        save_commit_activity(settings, dataframe)
        save_test_activity(settings, dataframe)

        show_commit_activity(dataframe)
        show_test_activity(dataframe)

    if args.commits:
        dataframe = analyze_commits(settings)
        save_commit_activity(settings, dataframe)
        show_commit_activity(dataframe)

    if args.test_activity:
        dataframe = analyze_commits(settings)
        show_test_activity(dataframe)
        save_test_activity(settings, dataframe)

    if args.churn:
        analyze_file_churn(settings)

    if args.churncomplexity:
        churn_complexity_frame = analyze_churn_complexity(settings)
        save_churn_complexity(churn_complexity_frame, settings)
        show_churn_complexity_chart(churn_complexity_frame)


def parse_arguments(args):
    """Parse the commandline arguments."""

    today = datetime.datetime.today()
    one_year_ago = today - datetime.timedelta(days=365)
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")

    parser.add_argument("repository", help="git repository to analyze")
    parser.add_argument("--output", help="directory where to place the report", default="./reports")

    parser.add_argument("--all", help="analyze all aspects", action="store_true")
    parser.add_argument("--churn", help="analyze the churn of the repository", action="store_true")
    parser.add_argument(
        "--churncomplexity", help="analyze the churn vs complexity for the repository", action="store_true"
    )
    parser.add_argument("--commits", help="analyze the commit activity of the repository", action="store_true")
    parser.add_argument("--test-activity", help="analyze the commits in test and production code", action="store_true")
    parser.add_argument(
        "--start-date", help="start date of the period to analyze", default=one_year_ago, action="store"
    )
    parser.add_argument("--end-date", help="end date of the period to analyze", default=today, action="store")
    parser.add_argument(
        "--frequency",
        choices=["DAILY", "WEEKLY", "MONTHLY", "YEARLY"],
        help=" the frequency of the analysis",
        default="WEEKLY",
        action="store",
    )

    parser.set_defaults(func=perform_analysis)

    return parser.parse_args(args)


def main():
    """Start of the program."""

    args = parse_arguments(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
