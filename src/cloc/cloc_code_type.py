"""Analyze the lines of code for all code types using the tool cloc."""
import csv
import os

from src.cloc.cloc_measure import measure_lines_of_code, get_size_metrics
from src.profile.colors import PROFILE_COLORS
from src.profile.show import make_donut
from src.reporting.reporting import create_report_directory


def write_code_size_metrics(csv_writer, metrics):
    """Write the code size metrics to the csv file."""

    language_metrics = metrics["SUM"]
    csv_writer.writerow(
        [
            language_metrics["blank"],
            language_metrics["code"],
            language_metrics["comment"],
        ]
    )


def write_code_size_header(csv_writer):
    """Write the header to the csv file."""

    csv_writer.writerow(
        [
            "Blank Lines",
            "Lines Of Code",
            "Comment Lines",
        ]
    )


def save_code_metrics(report_file, metrics):
    """Save the code metrics to a file."""

    with open(report_file, "w", encoding="utf-8") as output:
        csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)

        write_code_size_header(csv_writer)
        write_code_size_metrics(csv_writer, metrics)


def save_code_type_profile(report_dir, metrics):
    """Save the code metrics to a file."""

    report_file = os.path.join(report_dir, "code_type_profile.csv")
    with open(report_file, "w", encoding="utf-8") as output:
        csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)

        write_code_type_header(csv_writer)
        write_code_type_metrics(csv_writer, metrics)


def write_code_type_metrics(csv_writer, metrics):
    """Save the code type metrics."""

    if metrics:
        csv_writer.writerow(
            [
                metrics["production"]["SUM"]["code"],
                metrics["test"]["SUM"]["code"],
                metrics["generated"]["SUM"]["code"],
                metrics["third_party"]["SUM"]["code"],
            ]
        )


def write_code_type_header(csv_writer):
    """Save the code type metrics header."""

    csv_writer.writerow(
        [
            "Production",
            "Test",
            "Generated",
            "Third Party",
        ]
    )


def show_code_type_profile(metrics):
    """Show the profile in a donut."""

    labels = ["Production", "Test", "Third Party", "Generated"]
    values = [
        metrics["production"]["SUM"]["code"],
        metrics["test"]["SUM"]["code"],
        metrics["third_party"]["SUM"]["code"],
        metrics["generated"]["SUM"]["code"],
    ]

    fig = make_donut(labels, values, "Code type breakdown", PROFILE_COLORS)
    fig.show()


def analyze_code_volume_per_code_type(settings, code_type):
    """Analyze the code volume per code type based on the settings and code type provided."""

    report_dir = create_report_directory(settings["report_directory"])
    report_file = os.path.join(report_dir, "metrics", f"{code_type}_code_volume_profile.csv")
    analysis_filter = settings[f"{code_type}_filter"]
    measure_lines_of_code(settings["analysis_directory"], report_file, analysis_filter)
    metrics = get_size_metrics(report_file)
    save_code_metrics(report_file, metrics)
    return metrics


def analyze_code_type(settings):
    """Analyze the code size for all code types."""

    metrics = {}
    report_dir = create_report_directory(os.path.join(settings["report_directory"], "profiles"))

    for code_type in settings["code_type"]:
        metrics[code_type] = analyze_code_volume_per_code_type(settings, code_type)

    save_code_type_profile(report_dir, metrics)
    show_code_type_profile(metrics)

    return metrics
