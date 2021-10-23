"""
Perform analysis on a codebase using the tool cloc (count lines of code).

It can perform the following analysis:
- code size
- language distribution

It provides metrics on file level.
"""
import argparse
import os
import sys
import configparser

from src.cloc.cloc_code_size import analyze_code_size
from src.cloc.cloc_languages import analyze_language


def get_settings(configuration_file, parser=None):
    """Get the configuration from the ini file."""
    settings = {}

    if os.path.exists(configuration_file):
        if parser:
            config = parser
        else:
            config = configparser.ConfigParser()
            config.read(configuration_file)

        code_types = []
        for code_type in config["code_type"]:
            code_types.append(code_type)
            settings[f"{code_type}_filter"] = config["filters"][f"{code_type}_filter"]

        settings["code_type"] = code_types
        settings["report_directory"] = config["reporting"]["directory"]
        settings["analysis_directory"] = config["analysis"]["directory"]

    return settings


def perform_analysis(analysis):
    """Perform the requested analysis."""

    settings = get_settings(analysis.config)

    if analysis.all:
        analyze_code_size(settings)
        analyze_language(settings)

    if analysis.code_size:
        analyze_code_size(settings)

    if analysis.language:
        analyze_language(settings)

    return settings


def parse_arguments(args):
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")
    parser.add_argument("input", help="directory to analyze")
    parser.add_argument("--output", help="The directory where to place the report", default="./reports")
    parser.add_argument("--config", help="The configuration file to use.", default="cloc_analysis.ini")

    parser.add_argument("--all", help="analyze all aspects", action="store_true")
    parser.add_argument("--code-size", help="analyze the code size", action="store_true")
    parser.add_argument("--language", help="analyze the code size per language", action="store_true")

    parser.set_defaults(func=perform_analysis)

    return parser.parse_args(args)


def main():
    """Start of the program."""

    args = parse_arguments(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
