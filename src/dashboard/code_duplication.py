"""Show the code duplication metric."""
import csv

from dash import dcc
from dash import html

from src.cpd.cpd_analysis import determine_colors

from src.profile.show import make_donut


def get_duplication_metrics(report_file, reader=None):
    """Get the language metrics from the report file."""

    metrics = {}

    with open(report_file, "r", newline="\n", encoding="utf-8") as csv_file:
        csv_reader = reader or csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            metrics["duplicated_loc"] = row["Duplicated Lines Of Code"]
            metrics["total_loc"] = row["Total Lines Of Code"]

    return metrics


def code_duplication():
    """Determine the code duplication."""

    report_file = "D:\\\\Projects\\github\\sqatt\\reports\\code_duplication.csv"

    metrics = get_duplication_metrics(report_file)

    content = html.Div(
        [html.H3("Code duplication"), dcc.Graph(id="code_duplication", figure=code_duplication_figure(metrics))],
    )
    return content


def code_duplication_figure(metrics):
    """Create the code duplication donut."""

    duplicated_loc = int(metrics["duplicated_loc"])
    total_loc = int(metrics["total_loc"])

    labels = ["Duplicated code", "Non duplicated code"]
    values = [duplicated_loc, (total_loc - duplicated_loc)]

    percentage = (duplicated_loc / total_loc) * 100

    colors = determine_colors(percentage)

    return make_donut(labels, values, "Code duplication", colors)
