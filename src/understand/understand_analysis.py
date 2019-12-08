"""
Perform analysis on a codebase using the tool understand.

It can perform the following analysis:
- code size
- complexity
- fan-in
- fan-out
- function size
- interface size

It provides metrics on function level and file level.
"""
import argparse
import sys
from src.understand.understand_file_metrics import collect_file_metrics
from src.understand.understand_function_size import analyze_function_size


def add_analysis_parser(subparsers):
    """Add argument parser for analysis."""

    parser = subparsers.add_parser("analysis", help="analysis commands")
    parser.add_argument("database", help="understand database to analyze")
    parser.add_argument("--output", help="directory where to place the report", default="./reports")

    parser.add_argument("--all", help="analyze all aspects", action="store_true")
    parser.add_argument("--code-size", help="analyze the code size", action="store_true")
    parser.add_argument("--complexity", help="analyze the complexity", action="store_true")
    parser.add_argument("--fan-in", help="analyze the fan-in", action="store_true")
    parser.add_argument("--fan-out", help="analyze the fan-out", action="store_true")
    parser.add_argument("--interface", help="analyze the interface size", action="store_true")
    parser.add_argument("--function-size", help="analyze the function size", action="store_true")
    parser.add_argument("--file-size", help="analyze the file size", action="store_true")

    parser.set_defaults(func=perform_analysis)


def add_metrics_parser(subparsers):
    """Add argument parser for metrics collection."""

    parser = subparsers.add_parser("metrics", help="available metrics commands")
    parser.add_argument("database", help="understand database to analyze")
    parser.add_argument("--output", help="directory where to place the metrics", default="./reports")

    parser.add_argument("--function", help="collect function metrics", action="store_true")

    parser.add_argument("--file", help="collect file metrics", action="store_true")
    parser.add_argument("--module", help="module to analyze")
    parser.add_argument(
        "--sort",
        help="sort on the specified metric",
        choices=[
            "MaxCyclomatic",
            "CountLine",
            "CountLineCode",
            "CountLineBlank",
            "CountLineComment",
            "CountLineInactive",
            "CountLinePreprocessor",
            "CountDeclFile",
            "CountDeclFunction",
            "CountDeclClass",
        ],
    )

    parser.set_defaults(func=collect_metrics)


def parse_arguments(args):
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")
    subparsers = parser.add_subparsers(help="available sub-commands")

    add_analysis_parser(subparsers)
    add_metrics_parser(subparsers)

    return parser.parse_args(args)


def analyze_code_size(database, output):
    """Analyze the code size."""
    print("Analyzing code size")
    print(database, output)


def analyze_complexity(database, output):
    """Analyze the complexity."""
    print("Analyzing complexity")
    print(database, output)


def analyze_fan_in(database, output):
    """Analyze the fan-in."""
    print("Analyzing the fan-in")
    print(database, output)


def analyze_fan_out(database, output):
    """Analyze the fan-out."""
    print("Analyzing the fan-out")
    print(database, output)


def analyze_file_size(database, output):
    """Analyze the file size."""
    print("Analyzing the file size")
    print(database, output)


def analyze_interface(database, output):
    """Analyze the interface."""
    print("Analyzing the interface")
    print(database, output)


def perform_analysis(analysis):
    """Perform the requested analysis."""
    print(analysis)

    if analysis.all:
        analyze_code_size(analysis.database, analysis.output)
        analyze_complexity(analysis.database, analysis.output)
        analyze_function_size(analysis.database, analysis.output)
        analyze_file_size(analysis.database, analysis.output)
        analyze_fan_in(analysis.database, analysis.output)
        analyze_fan_out(analysis.database, analysis.output)
        analyze_interface(analysis.database, analysis.output)

    if analysis.code_size:
        analyze_code_size(analysis.database, analysis.output)

    if analysis.complexity:
        analyze_complexity(analysis.database, analysis.output)

    if analysis.function_size:
        analyze_function_size(analysis.database, analysis.output)

    if analysis.file_size:
        analyze_file_size(analysis.database, analysis.output)

    if analysis.fan_in:
        analyze_fan_in(analysis.database, analysis.output)

    if analysis.fan_out:
        analyze_fan_out(analysis.database, analysis.output)

    if analysis.interface:
        analyze_interface(analysis.database, analysis.output)


def collect_function_metrics(database, output):
    """Collect the function metrics."""
    print("Collecting function metrics")
    print(database, output)


def collect_metrics(metrics):
    """Collect the requested metrics."""

    print(metrics)

    if metrics.file:
        collect_file_metrics(metrics.database, metrics.output, metrics.module, metrics.sort)

    if metrics.function:
        collect_function_metrics(metrics.database, metrics.output)


def main():
    """Start of the program."""

    args = parse_arguments(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
