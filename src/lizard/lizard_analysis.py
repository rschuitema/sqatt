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
import sys

from src.lizard.lizard_function_complexity import analyze_complexity
from src.lizard.lizard_function_parameters import analyze_function_parameters
from src.lizard.lizard_function_size import analyze_function_size


def perform_analysis(analysis):
    """Perform the requested analysis."""
    print(analysis)

    if analysis.all:
        analyze_complexity(analysis.input, analysis.output)
        analyze_function_size(analysis.input, analysis.output)
        analyze_function_parameters(analysis.input, analysis.output)

    if analysis.complexity:
        analyze_complexity(analysis.input, analysis.output)

    if analysis.function_size:
        analyze_function_size(analysis.input, analysis.output)

    if analysis.interface:
        analyze_function_parameters(analysis.input, analysis.output)


def add_analysis_parser(subparsers):
    """Add argument parser for analysis."""

    parser = subparsers.add_parser("analysis", help="analysis commands")
    parser.add_argument("input", help="directory to analyze")
    parser.add_argument("--output", help="directory where to place the report", default="./reports")

    parser.add_argument("--all", help="analyze all aspects", action="store_true")
    parser.add_argument("--complexity", help="analyze the complexity of the code", action="store_true")
    parser.add_argument("--interface", help="analyze the interface size", action="store_true")
    parser.add_argument("--function-size", help="analyze the function size", action="store_true")
    parser.add_argument("--code-size", help="analyze the code size", action="store_true")

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
