"""
Perform analysis on a codebase using the tool lizard.

It can perform the following analysis:
- code size
- complexity
- number of parameters
- function size

It provides metrics on file level.
"""
import argparse
import csv
import os
import sys

from src.facility.subprocess import Subprocess

from src.profile.show import show_profile
from src.profile.sqatt_profiles import (
    create_function_size_profile,
    create_complexity_profile,
    create_function_parameters_profile,
)
from src.reporting.reporting import create_report_directory


def create_profiles():
    """Create all the metric profiles."""

    profiles = {
        "function_size": create_function_size_profile(),
        "complexity": create_complexity_profile(),
        "parameters": create_function_parameters_profile(),
    }

    return profiles


def determine_profiles(profiles, metrics_file, reader=None):
    """Determine the profile for the metrics: function size, complexity and number of parameters."""

    with open(metrics_file, "r", newline="\n", encoding="utf-8") as csv_file:
        csv_reader = reader or csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            profiles["function_size"].update(int(row[0]), int(row[0]))
            profiles["complexity"].update(int(row[1]), int(row[0]))
            profiles["parameters"].update(int(row[3]), int(row[0]))


def measure_function_metrics(input_dir, output_dir):
    """Measure the function metrics."""

    function_metrics_file = os.path.join(output_dir, "function_metrics.csv")

    measure_function_size_command = [
        "lizard",
        "--csv",
        f"-o{function_metrics_file}",
        input_dir,
    ]

    process = Subprocess(measure_function_size_command, verbose=3)
    process.execute()

    return function_metrics_file


def perform_analysis(analysis):
    """Perform the requested analysis."""

    report_dir = create_report_directory(analysis.output)
    metrics_file = measure_function_metrics(analysis.input, report_dir)
    profiles = create_profiles()
    determine_profiles(profiles, metrics_file)

    function_size_profile_file = os.path.join(report_dir, "function_size_profile.csv")
    complexity_profile_file = os.path.join(report_dir, "complexity_profile.csv")
    parameters_profile_file = os.path.join(report_dir, "parameters_profile.csv")

    if analysis.all:
        profiles["function_size"].print()
        profiles["complexity"].print()
        profiles["parameters"].print()

        profiles["function_size"].save(function_size_profile_file)
        profiles["complexity"].save(complexity_profile_file)
        profiles["parameters"].save(parameters_profile_file)
        show_profile(profiles["function_size"])
        show_profile(profiles["complexity"])
        show_profile(profiles["parameters"])

    if analysis.complexity:
        profiles["complexity"].print()
        profiles["complexity"].save(complexity_profile_file)
        show_profile(profiles["complexity"])

    if analysis.function_size:
        profiles["function_size"].print()
        profiles["function_size"].save(function_size_profile_file)
        show_profile(profiles["function_size"])

    if analysis.parameters:
        profiles["parameters"].print()
        profiles["parameters"].save(parameters_profile_file)
        show_profile(profiles["parameters"])


def parse_arguments(args):
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")

    parser.add_argument("input", help="directory to analyze")
    parser.add_argument("--output", help="directory where to place the report", default="./reports")

    parser.add_argument("--all", help="analyze all aspects", action="store_true")
    parser.add_argument("--complexity", help="analyze the complexity of the code", action="store_true")
    parser.add_argument("--parameters", help="analyze the interface size", action="store_true")
    parser.add_argument("--function-size", help="analyze the function size", action="store_true")

    parser.set_defaults(func=perform_analysis)

    return parser.parse_args(args)


def main():
    """Start of the program."""

    args = parse_arguments(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
