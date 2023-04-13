"""Analyze the code volume."""
import csv
import os

from src.profile.colors import PROFILE_COLORS
from src.profile.show import make_donut


def write_code_volume_header(csv_writer):
    """Write the header to the csv file."""

    csv_writer.writerow(
        [
            "Blank Lines",
            "Lines Of Code",
            "Comment Lines",
        ]
    )


def write_code_volume_metrics(csv_writer, metrics):
    """Save the code volume metrics."""

    if metrics:
        csv_writer.writerow(
            [
                metrics["Blank Lines"],
                metrics["Lines Of Code"],
                metrics["Comment Lines"],
            ]
        )


def read_code_volume(report_file, reader=None):
    """Read the code volume from a file."""

    code_volume = {}

    with open(report_file, "r", newline="\n", encoding="utf-8") as csv_file:
        csv_reader = reader or csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            code_volume["Blank Lines"] = int(row["Blank Lines"])
            code_volume["Lines Of Code"] = int(row["Lines Of Code"])
            code_volume["Comment Lines"] = int(row["Comment Lines"])

    return code_volume


def determine_total_code_volume(settings, code_volume):
    """Determine the total code volume based upon the code volume for each code type."""

    total_volume = {"Blank Lines": 0, "Lines Of Code": 0, "Comment Lines": 0}

    for code_type in settings["code_type"]:
        total_volume["Blank Lines"] = total_volume["Blank Lines"] + code_volume[code_type]["Blank Lines"]
        total_volume["Lines Of Code"] = total_volume["Lines Of Code"] + code_volume[code_type]["Lines Of Code"]
        total_volume["Comment Lines"] = total_volume["Comment Lines"] + code_volume[code_type]["Comment Lines"]

    return total_volume


def save_code_volume_profile(report_dir, metrics):
    """Save the code volume metrics to a file."""

    report_file = os.path.join(report_dir, "profiles", "code_volume_profile.csv")
    with open(report_file, "w", encoding="utf-8") as output:
        csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)

        write_code_volume_header(csv_writer)
        write_code_volume_metrics(csv_writer, metrics)


def show_code_volume_profile(metrics):
    """Show the profile in a donut."""

    labels = ["Blank Lines", "Lines Of Code", "Comment Lines"]
    values = [
        metrics["Blank Lines"],
        metrics["Lines Of Code"],
        metrics["Comment Lines"],
    ]

    fig = make_donut(labels, values, "Code volume breakdown", PROFILE_COLORS)
    fig.show()


def calculate_comment_to_code_ratio(code_volume):
    """Calculate the ratio between the comments and the lines of code."""

    total_lines = code_volume["Comment Lines"] + code_volume["Lines Of Code"]
    return float(code_volume["Comment Lines"]) / float(total_lines)


def calculate_test_code_to_production_code_ratio(production_code_metrics, test_code_metrics):
    """Calculate the ratio between the test code and the production code."""

    lines_of_code = production_code_metrics["Lines Of Code"]
    lines_of_test_code = test_code_metrics["Lines Of Code"]

    return float(lines_of_test_code) / float(lines_of_code)


def save_code_ratios(settings, comment_code_ratio, test_code_ratio):
    """Save the code ratios to a file in the directory specified by the settings."""

    report_file = os.path.join(settings["report_directory"], "profiles", "code_volume_ratios.csv")

    with open(report_file, "w", encoding="utf-8") as output:
        csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)

        csv_writer.writerow(["Comment To Code Ratio", "Test Code To Production Code Ratio"])
        csv_writer.writerow([comment_code_ratio, test_code_ratio])


def analyze_code_volume(settings):
    """Analyze the code volume. Measure the blank lines, comment lines, code lines."""

    code_volume = {}
    for code_type in settings["code_type"]:
        report_file = os.path.join(settings["report_directory"], "metrics", f"{code_type}_code_volume_profile.csv")
        code_volume_per_code_type = read_code_volume(report_file)
        code_volume[code_type] = code_volume_per_code_type

    total_code_volume = determine_total_code_volume(settings, code_volume)
    save_code_volume_profile(settings["report_directory"], total_code_volume)
    show_code_volume_profile(total_code_volume)

    comment_code_ratio = calculate_comment_to_code_ratio(total_code_volume)
    test_code_ratio = calculate_test_code_to_production_code_ratio(code_volume["production"], code_volume["test"])
    save_code_ratios(settings, comment_code_ratio, test_code_ratio)
