"""
Perform analysis on a codebase using the tool cloc (count lines of code).

It can perform the following analysis:
- lines of code per code type (Production, Test, Generated, Third party)
- lines of code per language
- code volume (blank lines, comment lines, code lines)
- lines of code per file

"""

import argparse
import sys

from src.cloc.cloc_analyze_file_size import analyze_file_size
from src.cloc.cloc_code_type import analyze_code_type
from src.cloc.cloc_code_volume import analyze_code_volume
from src.cloc.cloc_languages import analyze_language
from src.cloc.cloc_settings import get_settings


def perform_analysis(analysis):
    """
    Perform the requested analysis.

    Note: the code volume analysis uses the results of the code type analysis.
    """

    settings = get_settings(analysis.config, analysis.output, analysis.input)

    if analysis.all:
        analyze_code_type(settings)
        analyze_code_volume(settings)
        analyze_language(settings)
        analyze_file_size(settings)

    if analysis.code_type:
        analyze_code_type(settings)

    if analysis.code_volume:
        analyze_code_type(settings)
        analyze_code_volume(settings)

    if analysis.file_size:
        analyze_file_size(settings)

    if analysis.language:
        analyze_language(settings)

    return settings


def parse_arguments(args):
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")
    parser.add_argument("input", help="The directory to analyze.")
    parser.add_argument("--output", help="The directory where to place the report(s).")
    parser.add_argument("--config", help="The configuration file to use.", default="cloc_analysis.ini")

    parser.add_argument("--all", help="Analyze all aspects.", action="store_true")
    parser.add_argument(
        "--code-type",
        help="Analyze the lined of code per type (production, test, third party, etc).",
        action="store_true",
    )
    parser.add_argument("--code-volume", help="Analyze the code volume.", action="store_true")
    parser.add_argument("--file-size", help="Analyze the lines of code per file.", action="store_true")
    parser.add_argument("--language", help="Analyze the lines of code per language.", action="store_true")

    parser.set_defaults(func=perform_analysis)

    return parser.parse_args(args)


def main():
    """Start of the program."""

    args = parse_arguments(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
