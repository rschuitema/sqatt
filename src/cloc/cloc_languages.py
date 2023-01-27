"""Analyze the code size per language using the tool cloc."""
import csv
import os

from src.cloc.cloc_measure import measure_lines_of_code, get_size_metrics
from src.profile.colors import PROFILE_COLORS
from src.profile.show import make_donut
from src.reporting.reporting import create_report_directory


def write_metrics(csv_writer, metrics):
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


def write_header(csv_writer):
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


def save_language_profile(production_code_size_file, production_code_metrics):
    """Save the code metrics to a file."""

    with open(production_code_size_file, "w", encoding="utf-8") as output:
        csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)

        write_header(csv_writer)
        write_metrics(csv_writer, production_code_metrics)


def show_language_profile(profile):
    """Show the profile in a donut."""

    labels = []
    values = []
    for language, metrics in profile.items():
        labels.append(language)
        values.append(metrics["code"])

    fig = make_donut(labels, values, "Language profile", PROFILE_COLORS)
    fig.show()


def analyze_language(settings):
    """Analyze the lines of code per language."""

    report_dir = create_report_directory(settings["report_directory"])
    report_file = os.path.join(report_dir, "language_profile.csv")
    measure_lines_of_code(settings["analysis_directory"], report_file, "--exclude-dir=test,tst")
    language_metrics = get_size_metrics(report_file)

    del language_metrics["SUM"]

    save_language_profile(report_file, language_metrics)
    show_language_profile(language_metrics)
