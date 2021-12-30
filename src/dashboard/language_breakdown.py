"""Show how many languages are used in the project."""
import csv

from dash import dcc
from dash import html

from src.profile.colors import PROFILE_COLORS
from src.profile.show import make_donut


def get_language_metrics(report_file, reader=None):
    """Get the language metrics from the report file."""

    metrics = {}

    with open(report_file, "r", newline="\n", encoding="utf-8") as csv_file:
        csv_reader = reader or csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            metrics[row["Language"]] = row["Lines Of Code"]

    return metrics


def language_breakdown():
    """Create the language break down."""

    report_file = "D:\\\\Projects\\github\\sqatt\\reports\\language_profile.csv"
    metrics = get_language_metrics(report_file)

    content = html.Div(
        [html.H3("Language breakdown"), dcc.Graph(id="language_breakdown", figure=language_breakdown_figure(metrics))],
    )
    return content


def language_breakdown_figure(metrics):
    """Create the figure to show the language break down."""

    labels = []
    values = []
    for language in metrics:
        labels.append(language)
        values.append(metrics[language])

    return make_donut(labels, values, "Language breakdown", PROFILE_COLORS)
