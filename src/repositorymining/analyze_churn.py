"""
Analyze the churn.

It can analyze:
* the churn of the files in the repository.
* the churn versus the complexity of the files in a repository.

For these analysis the following metrics are needed:
* Churn
* Complexity
* Lines of code
* Number of functions

The churn is measured using the Pydriller library.
The other metrics are measured with the tool Lizard.

Churn versus complexity
-----------------------
This analysis is based upon the idea from the book: Legacy code - First Aid kit by Nicolas Carlo.
It is visualized with a bubble chart in which:
* the x-axis represents the churn
* the y-axis represents the complexity
* the size of the bubble represents the lines of code
* the color of the bubble represents the number of functions

The raw data is saved in a csv file called churn_complexity.csv in the specified reports directory.

Churn
-----
This analysis uses the PyDriller library and stores the raw data in a csv file called churn.csv
"""

import csv
import os

import plotly.graph_objects as go
import pandas as pd
from pydriller.metrics.process.code_churn import CodeChurn

from src.facility.subprocess import Subprocess
from src.reporting.reporting import create_report_directory


def measure_file_complexity(settings):
    """Measure file complexity metrics."""

    report_dir = create_report_directory(settings["report_directory"])

    function_metrics_file = os.path.join(report_dir, "function_metrics.xml")

    measure_function_size_command = [
        "lizard",
        "--xml",
        f"-o{function_metrics_file}",
        settings["repository"],
    ]

    process = Subprocess(measure_function_size_command, verbose=3)
    process.execute()

    return function_metrics_file


def show_churn_complexity_chart(total_frame):
    """
    Show a bubble chart with churn, complexity, lines of code and number of functions per analyzed file.

    The x-axis represents the churn of the file.
    The y-axis represents the complexity of the file.
    The size of the bubble represents the lines of code of the file.
    The color of the bubble represents the number of function in the file.
    """

    fig = go.Figure(
        data=[
            go.Scatter(
                x=total_frame["Churn"],
                y=total_frame["CCN"],
                text=total_frame["File"],
                hovertemplate="<b>%{text}</b><br><br>"
                + "Churn: %{x:.0f}<br>"
                + "CCN: %{y:.0f}<br>"
                + "NCSS: %{marker.size:,}<br>"
                + "#Functions: %{marker.color:,}"
                + "<extra></extra>",
                mode="markers",
                marker={
                    "color": total_frame["Functions"],
                    "colorbar": {"title": "Nr of Functions"},
                    "size": total_frame["NCSS"],
                    "sizemode": "area",
                    "sizeref": 2.0 * max(total_frame["NCSS"]) / (70.0**2),
                    "colorscale": ["green", "yellow", "orange", "red"],
                    "showscale": True,
                },
            )
        ]
    )

    fig.update_layout(
        xaxis_title={"text": "Churn"},
        yaxis_title={"text": "CCN"},
        title={"text": "Churn vs. Complexity", "y": 0.9, "x": 0.5, "xanchor": "center", "yanchor": "top"},
    )
    fig.show()


def measure_file_churn(settings):
    """Measure the churn of files in the repository."""

    directory = settings["repository"]
    metric = CodeChurn(
        path_to_repo=settings["repository"],
        since=settings["period_start"],
        to=settings["period_end"],
        add_deleted_lines_to_churn=True,
    )
    file_churn_map = {}
    for file_name in metric.files.items():
        if file_name is None:
            continue
        file_churn = sum(metric.files[file_name])
        file_churn_map[os.path.join(directory, file_name)] = file_churn

    sorted_churn = sorted(file_churn_map.items(), key=lambda item: item[1], reverse=True)
    return sorted_churn


def read_file_churn(settings):
    """Read the file churn from file and return a panda data frame."""

    churn_file = os.path.join(settings["report_directory"], "churn.csv")
    churn_frame = pd.read_csv(churn_file)
    return churn_frame


def read_file_complexity(settings):
    """Read the file complexity from file and return a panda data frame."""

    complexity_file = os.path.join(settings["report_directory"], "function_metrics.xml")
    complexity_frame = pd.read_xml(
        complexity_file,
        xpath='//cppncss/measure[contains(@type,"File")]/item',
        names=["File", "Nr", "NCSS", "CCN", "Functions"],
    )
    complexity_frame.drop(columns=["Nr"], inplace=True)
    return complexity_frame


def save_churn_complexity(total_frame, settings):
    """Save the churn complexity to a csv file."""

    report_dir = create_report_directory(settings["report_directory"])
    total_frame.to_csv(os.path.join(report_dir, "complexity_churn.csv"))


def analyze_churn_complexity(settings):
    """Analyze the churn complexity of each source file in the repository."""

    analyze_file_churn(settings)
    measure_file_complexity(settings)

    churn_frame = read_file_churn(settings)
    complexity_frame = read_file_complexity(settings)

    total_frame = complexity_frame.merge(churn_frame, how="left", left_on="File", right_on="File")
    return total_frame


def analyze_file_churn(settings):
    """Analyze the file churn of a repository."""

    report_dir = create_report_directory(settings["report_directory"])
    file_churn_map = measure_file_churn(settings)
    save_file_churn(report_dir, file_churn_map)


def write_file_churn_header(csv_writer):
    """Save the churn metrics header."""

    csv_writer.writerow(["File", "Churn"])


def write_file_churn_metrics(csv_writer, churn):
    """Save the file churn data."""

    for item in churn:
        file_name, file_churn = item
        if file_name is None:
            file_name = "Unknown"
        csv_writer.writerow([file_name, file_churn])


def save_file_churn(report_dir, churn):
    """Save the file churn metrics to a file."""

    report_file = os.path.join(report_dir, "churn.csv")
    with open(report_file, "w", encoding="utf-8") as output:
        csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)

        write_file_churn_header(csv_writer)
        write_file_churn_metrics(csv_writer, churn)
