"""Measure the lines of code."""
import csv
import os

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


def measure_loc(config, code_type):
    """Measure the code size."""

    report_dir = config["reporting"]["directory"]
    report_file = os.path.join(report_dir, f"{code_type}_profile.csv")

    command = [
        "cloc",
        "--csv",
        "--hide-rate",
        "--quiet",
        config["filters"][f"{code_type}_filter"],
        config["analysis"]["directory"],
    ]

    process = Subprocess(command)
    output = process.execute_pipe(report_dir, report_file)

    return output


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
