"""
Perform analysis on a codebase using the tool cloc (count lines of code).

It can perform the following analysis:
- code size
- language distribution

It provides metrics on file level.
"""
import argparse
import sys

from src.cloc.cloc_code_size import analyze_code_size


def perform_analysis(analysis):
    """Perform the requested analysis."""
    print(analysis)

    if analysis.all:
        analyze_code_size(analysis.input, analysis.output)

    if analysis.code_size:
        analyze_code_size(analysis.input, analysis.output)


def add_analysis_parser(subparsers):
    """Add argument parser for analysis."""

    parser = subparsers.add_parser("analysis", help="analysis commands")
    parser.add_argument("input", help="directory to analyze")
    parser.add_argument(
        "--output", help="directory where to place the report", default="./reports"
    )

    parser.add_argument("--all", help="analyze all aspects", action="store_true")
    parser.add_argument(
        "--code-size", help="analyze the code size", action="store_true"
    )

    parser.set_defaults(func=perform_analysis)


def parse_arguments(args):
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")
    subparsers = parser.add_subparsers(help="available sub-commands")

    add_analysis_parser(subparsers)

    return parser.parse_args(args)


def main():
    """Start of the program."""

    args = parse_arguments(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
