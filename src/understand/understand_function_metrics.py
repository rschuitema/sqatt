"""Retrieve all function metrics of the codebase."""

import argparse
import csv
import os
import understand


def parse_arguments():
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="understand database to parse")
    parser.add_argument("--reportdir", help="directory where to place the report")
    args = parser.parse_args()
    return args


def create_report_directory(directory):
    """Create the report directory."""

    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def main():
    """The main entry point of the program."""

    args = parse_arguments()
    understand_database = args.input

    understand_database = understand.open(understand_database)

    report_file = os.path.join(create_report_directory(args.reportdir), "function_metrics.csv")
    with open(report_file, 'w') as output:
        csv_writer = csv.writer(output, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL)
        csv_writer.writerow(['FunctionName',
                             'LinesOfCode',
                             'CyclomaticComplexity',
                             'Fan-in',
                             'Fan-out',
                             'NumberOfParameters'])

        for func in understand_database.ents("function,method,procedure"):
            metrics = func.metric(["CountLineBlank",
                                   "CountLineCode",
                                   "CountLineComment",
                                   "CountLineInactive",
                                   "Cyclomatic",
                                   "CountInput",
                                   "CountOutput"])

            csv_writer.writerow([func.longname(),
                                 metrics["CountLineCode"],
                                 metrics["Cyclomatic"],
                                 metrics["CountInput"],
                                 metrics["CountOutput"],
                                 len(func.parameters().split(","))])


if __name__ == "__main__":
    main()
