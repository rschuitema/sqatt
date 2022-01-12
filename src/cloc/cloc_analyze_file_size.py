"""Analyze the file size using the tool cloc."""
import csv
import os

from src.facility.subprocess import Subprocess
from src.reporting.reporting import create_report_directory


def measure_file_size(input_dir, report_file, measure_filter):
    """Measure the lines of code per file using a filter."""

    measure_file_size_command = [
        "cloc",
        "--by-file",
        "--csv",
        "--csv-delimiter=,",
        "--hide-rate",
        f"--report-file={report_file}",
        measure_filter,
        input_dir,
    ]

    process = Subprocess(measure_file_size_command, verbose=1)
    process.execute()


def get_file_size_metrics(report_file, reader=None):
    """Get the file size metrics from file."""

    metrics = {}

    with open(report_file, "r", newline="\n", encoding="utf-8") as csv_file:
        csv_reader = reader or csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            file_metric = {
                "language": row["language"],
                "blank": row["blank"],
                "comment": row["comment"],
                "code": row["code"],
            }
            metrics[row["filename"]] = file_metric

    return metrics


def write_file_size_header(csv_writer):
    """Save the code type metrics header."""

    csv_writer.writerow(
        [
            "Filename",
            "Blank Lines",
            "Lines of Code",
            "Comment Lines",
        ]
    )


def write_file_size_metrics(csv_writer, metrics):
    """Save the file size metrics."""

    for filename in metrics:
        csv_writer.writerow(
            [
                filename,
                metrics[filename]["Blank Lines"],
                metrics[filename]["Lines of Code"],
                metrics[filename]["Comment Lines"],
            ]
        )


def save_file_profile(metrics, report_dir):
    """Save the file metrics to a file."""

    report_file = os.path.join(report_dir, "file_size_profile.csv")
    with open(report_file, "w", encoding="utf-8") as output:
        csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)

        write_file_size_header(csv_writer)
        write_file_size_metrics(csv_writer, metrics)


def analyze_file_size(settings):
    report_dir = create_report_directory(settings["report_directory"])
    report_file = os.path.join(report_dir, "file_size_raw.csv")
    analysis_filter = settings["file_size_filter"]

    measure_file_size(settings["analysis_directory"], report_file, analysis_filter)
    metrics = get_file_size_metrics(report_file)

    save_file_profile(metrics, report_dir)
