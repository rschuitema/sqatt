"""Calculate metrics from data in Jira."""

import argparse
import sys

from src.jira.age import analyze_issue_age
from src.jira.pmi import calculate_pmi, show_pmi


def parse_arguments(args):
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")
    parser.add_argument("--pmi", help="Calculate the PMI", action="store_true")
    parser.add_argument("--age", help="Analyze issue age", action="store_true")
    parser.add_argument("url", help="The url to the Jira database")
    parser.add_argument("username", help="The Jira username")
    parser.add_argument("password", help="The Jira password")

    return parser.parse_args(args)


def main():
    """Start of the program."""

    args = parse_arguments(sys.argv[1:])

    if args.age:
        analyze_issue_age(args.url, args.username, args.password)

    if args.pmi:
        calculate_pmi(args.url, args.username, args.password)
        show_pmi()


if __name__ == "__main__":
    main()
