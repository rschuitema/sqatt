"""Show the code break down metrics: code volume, code type."""
import csv
import os.path

import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

from src.profile.colors import profile_colors
from src.profile.show import make_donut


def get_production_code_size_metrics(report_directory, reader=None):
    """Get the production code size metrics from the report file."""

    metrics = {}
    report_file = os.path.join(report_directory, "production_code_volume_profile.csv")
    with open(report_file, "r", newline="\n", encoding="utf-8") as csv_file:
        csv_reader = reader or csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            metrics["Blank Lines"] = row["Blank Lines"]
            metrics["Lines Of Code"] = row["Lines Of Code"]
            metrics["Comment Lines"] = row["Comment Lines"]

    return metrics


def code_volume_breakdown(report_directory):
    """Determine the code volume."""

    metrics = get_production_code_size_metrics(report_directory)

    labels = ["Blank Lines", "Lines of Code", "Comment Lines"]
    values = [
        metrics["Blank Lines"],
        metrics["Lines Of Code"],
        metrics["Comment Lines"],
    ]

    return make_donut(labels, values, "Code volume <br> breakdown", profile_colors)


def get_code_type_metrics(report_directory, reader=None):
    """Get the code type metrics from the report file."""

    metrics = {}
    report_file = os.path.join(report_directory, "code_type_profile.csv")

    with open(report_file, "r", newline="\n", encoding="utf-8") as csv_file:
        csv_reader = reader or csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            metrics["production"] = row["Production"]
            metrics["test"] = row["Test"]
            metrics["generated"] = row["Generated"]
            metrics["third_party"] = row["Third Party"]

    return metrics


def code_type_breakdown(report_directory):
    """Determine the code type."""
    metrics = get_code_type_metrics(report_directory)

    labels = ["Production", "Test", "Third Party", "Generated"]
    values = [
        metrics["production"],
        metrics["test"],
        metrics["third_party"],
        metrics["generated"],
    ]

    return make_donut(labels, values, "Code type <br> breakdown", profile_colors)


def code_breakdown_settings():
    """Provide the settings for the code breakdown analysis."""

    settings = {
        "report_directory": "D:\\\\Projects\\github\\sqatt\\reports",
        "analysis_directory": "D:\\\\Projects\\github\\sqatt",
        "code_type": ["production", "test", "third_party", "generated"],
        "production_filter": "--exclude-dir=test,tst,jira,resharper",
        "test_filter": "--match-d=(test|tst)",
        "third_party_filter": "--match-d=(external|ext|jira)",
        "generated_filter": "--match-d=(generated|gen|resharper)",
    }
    return settings


def code_breakdown():
    """Show the code break down."""

    report_directory = "D:\\\\Projects\\github\\sqatt\\reports"
    container = html.Div(
        [
            html.H3("Code type breakdown"),
            dbc.Row(dbc.Col(dcc.Graph(id="code_type", figure=code_type_breakdown(report_directory)))),
            html.H3("Code volume breakdown"),
            dbc.Row(dbc.Col(dcc.Graph(id="code_volume", figure=code_volume_breakdown(report_directory)))),
        ]
    )
    return container
