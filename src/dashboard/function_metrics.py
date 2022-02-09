"""Show the function metrics: complexity, function size and function parameters."""
import csv
import os

from dash import dcc
from dash import html

import plotly.graph_objects as go
from src.profile.colors import PROFILE_COLORS


def get_complexity_metrics(reader=None):
    """Get the complexity metrics from the report file."""

    metrics = {}
    report_file = "D:\\\\Projects\\github\\sqatt\\reports\\complexity_profile.csv"

    with open(report_file, "r", newline="\n", encoding="utf-8") as csv_file:
        csv_reader = reader or csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            metrics[row["Complexity"]] = row["Lines Of Code"]

    return metrics


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
                title=dict(text=title),
                labels=labels,
                values=values,
                hole=0.5,
                marker_colors=colors,
                marker_line=dict(color="white", width=2),
            )
        ]
    )

    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.2))

    return fig


def get_function_size_metrics(reader=None):
    """Get the language metrics from the report file."""

    metrics = {}
    report_file = "D:\\\\Projects\\github\\sqatt\\reports\\function_size_profile.csv"

    with open(report_file, "r", newline="\n", encoding="utf-8") as csv_file:
        csv_reader = reader or csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            metrics[row["Function size"]] = row["Lines Of Code"]

    return metrics


def get_parameters_metrics(reader=None):
    """Get the language metrics from the report file."""

    metrics = {}
    report_file = "D:\\\\Projects\\github\\sqatt\\reports\\function_parameters_profile.csv"

    with open(report_file, "r", newline="\n", encoding="utf-8") as csv_file:
        csv_reader = reader or csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            metrics[row["Function parameters"]] = row["Lines Of Code"]

    return metrics


def get_metrics(name, reader=None):
    """Get the language metrics from the report file."""

    metrics = {}
    report_directory = "D:\\\\Projects\\github\\sqatt\\reports\\"
    report_file = os.path.join(report_directory, f'{name.lower().replace(" ", "_")}_profile.csv')

    with open(report_file, "r", newline="\n", encoding="utf-8") as csv_file:
        csv_reader = reader or csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            metrics[row[name]] = row["Lines Of Code"]

    return metrics


def function_metrics():
    """Determine the function metrics."""

    container = html.Div(
        [
            html.H3("Complexity"),
            dcc.Graph(id="complexity", figure=make_my_profile(get_metrics("Complexity"), "Complexity")),
            html.H3("Function size"),
            dcc.Graph(id="function_size", figure=make_my_profile(get_metrics("Function size"), "Function size")),
            html.H3("Function parameters"),
            dcc.Graph(
                id="function_parameters",
                figure=make_my_profile(get_metrics("Function parameters"), "Function parameters")
            ),
        ]
    )
    return container
