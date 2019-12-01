"""Create a profile for the code size."""

import argparse
import csv
import os
import re
import understand

from src.understand.understand_report import create_report_directory


def parse_arguments():
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("database", help="understand database to parse")
    parser.add_argument("--reportdir", default=".", help="directory where to place the report")
    args = parser.parse_args()
    return args


def measure_test_code_size(database):
    """Get the number of lines of code used for test cdoe."""

    metrics = {}
    search_str = re.compile(r"test", re.I)
    for file in database.lookup(search_str, "File"):
        file_metrics = file.metric(
            [
                "CountLine",
                "CountLineBlank",
                "CountLineCode",
                "CountLineComment",
                "CountLineInactive",
                "CountLinePreprocessor",
                "CountDeclFunction",
                "CountDeclClass",
            ]
        )

        metrics[file.longname()] = file_metrics

    return metrics


def save_test_code_size(metrics, report_dir):
    """Save the test code size to a csv file."""

    report_file = os.path.join(report_dir, "test_code_size.csv")
    with open(report_file, "w") as output:
        csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)
        csv_writer.writerow(
            [
                "File Name",
                "Total Lines",
                "Blank Lines",
                "Lines Of Code",
                "Comment Lines",
                "Inactive Lines",
                "Preprocessor Lines",
                "Number Of Functions",
                "Number Of Classes",
            ]
        )

        for filename in metrics:
            file_metrics = metrics[filename]

            csv_writer.writerow(
                [
                    filename,
                    file_metrics["CountLine"],
                    file_metrics["CountLineBlank"],
                    file_metrics["CountLineCode"],
                    file_metrics["CountLineComment"],
                    file_metrics["CountLinePreprocessor"],
                    file_metrics["CountDeclFunction"],
                    file_metrics["CountDeclClass"],
                ]
            )


def print_test_code_ratio(metrics, test_metrics):
    """Print the ration between test code size and production code size."""

    lines_of_code = metrics["CountLineCode"]
    lines_of_test_code = 0

    for filename in test_metrics:
        file_metrics = test_metrics[filename]
        lines_test_code = file_metrics["CountLineCode"]
        if lines_test_code is not None:
            lines_of_test_code = lines_of_test_code + lines_test_code

    print("Lines of code: {}".format(lines_of_code))
    print("Lines of test code: {}".format(lines_of_test_code))
    print("Ratio: {0:.2f}".format(100 * lines_of_test_code / lines_of_code))


def save_code_size(metrics, report_dir):
    """Save the production code size to a csv file."""

    report_file = os.path.join(report_dir, "code_size.csv")
    with open(report_file, "w") as output:
        csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)
        csv_writer.writerow(
            [
                "Total Lines",
                "Blank Lines",
                "Lines Of Code",
                "Comment Lines",
                "Inactive Lines",
                "Preprocessor Lines",
                "Number Of Files",
                "Number Of Functions",
                "Number Of Classes",
            ]
        )

        csv_writer.writerow(
            [
                metrics["CountLine"],
                metrics["CountLineBlank"],
                metrics["CountLineCode"],
                metrics["CountLineComment"],
                metrics["CountLinePreprocessor"],
                metrics["CountDeclFile"],
                metrics["CountDeclFunction"],
                metrics["CountDeclClass"],
            ]
        )


def measure_code_size(understand_database):
    """Get the number of lines of code for the production code."""

    metrics = understand_database.metric(
        [
            "CountLine",
            "CountLineBlank",
            "CountLineCode",
            "CountLineComment",
            "CountLineInactive",
            "CountLinePreprocessor",
            "CountDeclFile",
            "CountDeclFunction",
            "CountDeclClass",
        ]
    )

    return metrics


def main():
    """Start of the program."""

    args = parse_arguments()
    understand_database = understand.open(args.database)

    reportdir = create_report_directory(args.reportdir)

    metrics = measure_code_size(understand_database)
    save_code_size(metrics, reportdir)

    test_metrics = measure_test_code_size(understand_database)
    save_test_code_size(test_metrics, reportdir)

    print_test_code_ratio(metrics, test_metrics)


if __name__ == "__main__":
    main()
