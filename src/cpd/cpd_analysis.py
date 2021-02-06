"""Analysis functions for the tool CPD."""

import argparse
import csv
import os
import sys

import plotly.graph_objects as go

from src.facility.subprocess import Subprocess
from src.reporting.reporting import create_report_directory


def measure_code_duplication(settings):
    """Measure the amount of code duplication."""

    report_dir = create_report_directory(settings["report_directory"])
    report_file = os.path.join(report_dir, "code_duplication")

    measure_function_size_command = [
        "cpd",
        "--language",
        settings["language"],
        "--minimum-tokens",
        settings["tokens"],
        "--format",
        "csv",
        "--files",
        settings["analysis_directory"],
    ]

    process = Subprocess(measure_function_size_command, verbose=1)
    output = process.execute_pipe(report_dir, report_file, check_return_code=False)

    return output.stdout.decode("utf-8")


def measure_lines_of_code(settings):
    """Measure the lines of code using cloc."""

    report_dir = create_report_directory(settings["report_directory"])
    report_file = os.path.join(report_dir, "code_duplication")

    command = [
        "cloc",
        "--csv",
        "--hide-rate",
        "--quiet",
        "--exclude-dir=test,tst",
        settings["analysis_directory"],
    ]

    process = Subprocess(command, verbose=1)
    output = process.execute_pipe(report_dir, report_file, check_return_code=False)

    return output.stdout.decode("utf-8")


def determine_duplicate_lines_of_code(csv_input):
    """Calculate the number of duplicated lines of code."""

    csv_data = csv_input.splitlines()
    data = csv.DictReader(csv_data)
    duplicate_loc = 0
    for row in data:
        duplicate_loc = duplicate_loc + (int(row["lines"]) * (int(row["occurrences"])))

    return duplicate_loc


def determine_total_lines_of_code(csv_input):
    """Determine the total lines of code."""

    csv_data = csv_input.splitlines()
    del csv_data[0]
    reader = csv.DictReader(csv_data)
    total_loc = 0
    for row in reader:
        if row["language"] == "SUM":
            total_loc = row["code"]

    return total_loc


def show_duplication_profile(total_loc, duplicated_loc):
    """Show the duplication profile in s donut."""

    labels = ["Duplicated code", "Non duplicated code"]
    values = [duplicated_loc, (total_loc - duplicated_loc)]

    percentage = (duplicated_loc / total_loc) * 100

    colors = determine_colors(percentage)

    fig = go.Figure(
        data=[
            go.Pie(
                title=dict(text="Code duplication"),
                labels=labels,
                values=values,
                hole=0.5,
                marker_colors=colors,
                marker_line=dict(color="white", width=2),
            )
        ]
    )

    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5))

    fig.show()


def determine_colors(percentage):
    """
    Determine the color of the duplicated section.

    The color depends on the amount of code duplication.
    """

    colors = []

    if 3 >= percentage > 0:
        colors.append("rgb(121, 185, 79)")
    elif 5 >= percentage > 3:
        colors.append("rgb(255, 204, 5)")
    elif 20 >= percentage > 5:
        colors.append("rgb(251, 135, 56)")
    else:
        colors.append("rgb(204, 5, 5)")

    colors.append("rgb(121, 185, 79)")

    return colors


def analyze_duplication(settings):
    """Analyze code duplication."""

    metrics = {}

    output = measure_code_duplication(settings)
    metrics["duplicated_loc"] = int(determine_duplicate_lines_of_code(output))

    output = measure_lines_of_code(settings)
    metrics["total_loc"] = int(determine_total_lines_of_code(output))

    return metrics


def perform_analysis(analysis):
    """Perform the requested analysis."""

    settings = {
        "analysis_directory": analysis.input,
        "report_directory": analysis.output,
        "tokens": analysis.tokens,
        "language": analysis.language,
    }

    output = measure_code_duplication(settings)
    duplicated_loc = int(determine_duplicate_lines_of_code(output))

    output = measure_lines_of_code(settings)
    total_loc = int(determine_total_lines_of_code(output))

    show_duplication_profile(total_loc, duplicated_loc)


def parse_arguments(args):
    """Parse the commandline arguments."""

    print(os.getcwd())
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")
    parser.add_argument(
        "--output", help="The directory where to place the report.", default=os.path.join(os.getcwd(), "reports")
    )
    parser.add_argument("--language", help="The language to analyze.", default="python", required=True)
    parser.add_argument(
        "--tokens", help="The minimum token length which should be reported as a duplicate.", default=100, required=True
    )
    parser.add_argument("input", help="The directory to analyze.")

    parser.set_defaults(func=perform_analysis)

    return parser.parse_args(args)


def main():
    """Start of the program."""

    args = parse_arguments(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
