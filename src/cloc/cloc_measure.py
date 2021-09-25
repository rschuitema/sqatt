"""Measure the lines of code."""
import csv
from src.facility.subprocess import Subprocess


def measure_lines_of_code(input_dir, report_file, measure_filter):
    """Measure the lines of code using a filter."""

    measure_language_size_command = [
        "cloc",
        "--csv",
        "--csv-delimiter=,",
        "--hide-rate",
        f"--report-file={report_file}",
        measure_filter,
        input_dir,
    ]

    process = Subprocess(measure_language_size_command, verbose=1)
    process.execute()


def get_size_metrics(report_file, reader=None):
    """Get the size metrics from file."""

    metrics = {}

    with open(report_file, "r", newline="\n", encoding="utf-8") as csv_file:
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
