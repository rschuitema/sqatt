"""Show the file size metric."""

import csv
import os

from dash import dcc
from dash import html

import plotly.graph_objects as go
from src.profile.colors import PROFILE_COLORS


def make_my_profile(metrics, name):
    """Make the profile."""
    labels = []
    values = []
    for metric, value in metrics.items():
        labels.append(metric)
        values.append(value)

    fig = make_donut(labels, values, name, PROFILE_COLORS)
    return fig


def make_donut(labels, values, title, colors):
    """Show the values in a donut."""

    fig = go.Figure(
        data=[
            go.Pie(
                title={"text": title},
                labels=labels,
                values=values,
                hole=0.5,
                marker_colors=colors,
                marker_line={"color": "white", "width": 2},
            )
        ]
    )

    fig.update_layout(legend={"orientation": "h", "yanchor": "bottom", "xanchor": "center", "x": 0.5, "y": -0.2})

    return fig


def get_file_size_metrics(reader=None):
    """Get the file size from the report file."""

    metrics = {}
    report_directory = "D:\\\\Projects\\github\\sqatt\\reports\\profiles"
    report_file = os.path.join(report_directory, "file_size_profile.csv")

    with open(report_file, "r", newline="\n", encoding="utf-8") as csv_file:
        csv_reader = reader or csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            metrics[row["File size"]] = row["Lines Of Code"]

    return metrics


def file_size_metrics():
    """Determine the function metrics."""

    container = html.Div(
        [
            html.H3("File size"),
            dcc.Graph(id="File size", figure=make_my_profile(get_file_size_metrics(), "File size")),
        ]
    )
    return container
