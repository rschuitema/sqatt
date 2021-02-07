"""Show the code break down metrics: code volume, code type."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from src.cloc.cloc_code_size import analyze_size

from src.profile.colors import profile_colors
from src.profile.show import make_donut


def code_volume_breakdown(metrics):
    """Determine the code volume."""

    labels = ["Blank Lines", "Lines of Code", "Comment Lines"]
    values = [
        metrics["production"]["SUM"]["blank"],
        metrics["production"]["SUM"]["code"],
        metrics["production"]["SUM"]["comment"],
    ]

    return make_donut(labels, values, "Code volume <br> breakdown", profile_colors)


def code_type_breakdown(metrics):
    """Determine the code type."""

    labels = ["Production", "Test", "Third Party", "Generated"]
    values = [
        metrics["production"]["SUM"]["code"],
        metrics["test"]["SUM"]["code"],
        metrics["third_party"]["SUM"]["code"],
        metrics["generated"]["SUM"]["code"],
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

    metrics = analyze_size(code_breakdown_settings())
    container = html.Div(
        [
            html.H3("Code type breakdown"),
            dbc.Row(dbc.Col(dcc.Graph(id="code_type", figure=code_type_breakdown(metrics)))),
            html.H3("Code volume breakdown"),
            dbc.Row(dbc.Col(dcc.Graph(id="code_volume", figure=code_volume_breakdown(metrics)))),
        ]
    )
    return container
