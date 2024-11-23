"""Determine the churn of files using git log."""

import argparse
import csv
import os
import sys
from collections import Counter
from src.facility.subprocess import Subprocess


def get_git_log(settings):
    """
    Get the git log file from the provided repository.

    The log file is retrieved from the date provided in the since setting.
    """

    log_directory = os.path.join(settings["report_directory"], "churn")
    os.makedirs(log_directory, exist_ok=True)

    log_file = os.path.join(log_directory, "churn.log")

    git_log_command = [
        "git",
        "-C",
        settings["repository"],
        "log",
        "--format=format:",
        "--name-only",
        f"--since={settings['since']}",
    ]

    process = Subprocess(git_log_command, verbose=1)
    output = process.execute_pipe(settings["report_directory"], log_file, check_return_code=True)
    return output.stdout.decode("utf-8")


def parse_arguments(args):
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()

    parser.add_argument("repository", help="git repository to analyze")
    parser.add_argument("--output", help="directory where to place the report", default="./reports")
    parser.add_argument("--since", help="start date of the period to analyze", default="1-1-2020", action="store")

    return parser.parse_args(args)


def get_settings(args):
    """Convert the command line arguments in to settings."""

    settings = {"repository": args.repository, "report_directory": args.output, "since": args.since}
    return settings


def remove_empty_lines(git_log):
    """Remove the empty lines form the log file."""

    return os.linesep.join([s for s in git_log.splitlines() if s])


def determine_churn(settings):
    """Determine the churn from the git log file."""

    git_log = get_git_log(settings)
    git_log = remove_empty_lines(git_log)
    churn = calculate_churn(git_log)
    return churn


def calculate_churn(git_log):
    """Calculate the churn and return a sorted list of the churn."""

    return Counter(git_log.splitlines()).most_common()


def save_churn(churn, report_directory):
    """Save the churn in a csv file in the churn subdirectory of the report directory."""

    churn_file = os.path.join(report_directory, "churn", "churn.csv")

    with open(churn_file, "w", encoding="utf8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["File", "Churn"])
        for row in churn:
            writer.writerow(list(row))


def main():
    """Start of the program."""

    args = parse_arguments(sys.argv[1:])
    settings = get_settings(args)
    os.makedirs(settings["report_directory"], exist_ok=True)
    churn = determine_churn(settings)
    save_churn(churn, settings["report_directory"])


if __name__ == "__main__":
    main()
