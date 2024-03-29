"""Create a profile for the code size."""

import csv
import os
import re
import understand

from src.reporting.reporting import create_report_directory


def measure_test_code_size(database):
    """Get the number of lines of code used for test code."""

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
    with open(report_file, "w", encoding="utf-8") as output:
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

    print(f"Lines of code: {lines_of_code}")
    print(f"Lines of test code: {lines_of_test_code}")
    print(f"Ratio: {100 * lines_of_test_code / lines_of_code:.2f}")


def save_code_size(metrics, report_dir):
    """Save the production code size to a csv file."""

    report_file = os.path.join(report_dir, "code_size.csv")
    with open(report_file, "w", encoding="utf-8") as output:
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
                metrics["CountLineInactive"],
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


def analyze_code_size(database, output):
    """Analyze the code size."""

    understand_database = understand.open(database)

    report_dir = create_report_directory(output)

    metrics = measure_code_size(understand_database)
    save_code_size(metrics, report_dir)

    test_metrics = measure_test_code_size(understand_database)
    save_test_code_size(test_metrics, report_dir)

    print_test_code_ratio(metrics, test_metrics)
