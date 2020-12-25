"""Analyze the code size using the tool cloc."""
import csv
import os

from src.facility.subprocess import Subprocess
from src.reporting.reporting import create_report_directory


def write_code_size_metrics(csv_writer, metrics):
    """Write the code size metrics to the csv file."""

    for language in metrics:
        language_metrics = metrics[language]
        csv_writer.writerow(
            [
                language,
                language_metrics["files"],
                language_metrics["blank"],
                language_metrics["code"],
                language_metrics["comment"],
            ]
        )


def write_code_size_header(csv_writer):
    """Write the header to the csv file."""

    csv_writer.writerow(
        [
            "Language",
            "Number Of Files",
            "Blank Lines",
            "Lines Of Code",
            "Comment Lines",
        ]
    )


def get_size_metrics(report_file, reader=None):
    """Get the size metrics from file."""

    metrics = {}

    with open(report_file, "r", newline="\n") as csv_file:
        csv_reader = reader or csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            language_metric = {
                "files": row["files"],
                "blank": row["blank"],
                "comment": row["comment"],
                "code": row["code"],
            }
            metrics[row["language"]] = language_metric

    return metrics


def calculate_comment_to_code_ratio(production_code_metrics, test_code_metrics):
    """Calculate the ratio between the comments and the lines of code."""

    lines_of_code = production_code_metrics["SUM"]["code"] + test_code_metrics["SUM"]["code"]
    comment_lines = production_code_metrics["SUM"]["comment"] + test_code_metrics["SUM"]["comment"]

    print(lines_of_code, comment_lines)

    return float(comment_lines) / float(lines_of_code)


def calculate_test_code_to_production_code_ratio(production_code_metrics, test_code_metrics):
    """Calculate the ratio between the test code and the production code."""

    lines_of_code = production_code_metrics["SUM"]["code"]
    lines_of_test_code = test_code_metrics["SUM"]["code"]

    return float(lines_of_test_code) / float(lines_of_code)


def save_code_metrics(production_code_size_file, production_code_metrics):
    """Save the code metrics to a file."""

    with open(production_code_size_file, "w") as output:
        csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)

        write_code_size_header(csv_writer)
        write_code_size_metrics(csv_writer, production_code_metrics)


def save_ratios(comment_code_ratio, test_code_ratio):
    """Save the metric ratios to a file."""

    print(comment_code_ratio, test_code_ratio)


def analyze_code_size(input_dir, output_dir):
    """Analyze the code size."""

    report_dir = create_report_directory(output_dir)

    production_code_size_file = os.path.join(report_dir, "production_code_size.csv")
    measure_production_code_size(input_dir, production_code_size_file)

    test_code_size_file = os.path.join(report_dir, "test_code_size.csv")
    measure_test_code_size(input_dir, test_code_size_file)

    production_code_metrics = get_size_metrics(production_code_size_file)
    test_code_metrics = get_size_metrics(test_code_size_file)

    comment_code_ratio = calculate_comment_to_code_ratio(production_code_metrics, test_code_metrics)
    test_code_ratio = calculate_test_code_to_production_code_ratio(production_code_metrics, test_code_metrics)

    save_code_metrics(production_code_size_file, production_code_metrics)
    save_code_metrics(test_code_size_file, test_code_metrics)

    save_ratios(comment_code_ratio, test_code_ratio)


def measure_production_code_size(input_dir, report_file):
    """Measure the production code size."""

    measure_language_size_command = [
        "cloc",
        "--csv",
        "--csv-delimiter=,",
        "--hide-rate",
        f"--report-file={report_file}",
        "--exclude-dir=test,tst",
        input_dir,
    ]

    process = Subprocess(measure_language_size_command, verbose=1)
    process.execute()


def measure_test_code_size(input_dir, report_file):
    """Measure the test code size."""

    measure_language_size_command = [
        "cloc",
        "--csv",
        "--csv-delimiter=,",
        "--hide-rate",
        f"--report-file={report_file}",
        "--match-d=/(test|tst)/",
        input_dir,
    ]

    process = Subprocess(measure_language_size_command, verbose=1)
    process.execute()
