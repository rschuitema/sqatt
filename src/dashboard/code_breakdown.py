"""Show the code break down metrics: code volume, code type."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go

from src.cloc.cloc_code_size import analyze_size

profile_colors = [
    "rgb(121, 185, 79)",
    "rgb(255, 204, 5)",
    "rgb(251, 135, 56)",
    "rgb(204, 5, 5)",
    "rgb(121,55,171)",
    "rgb(255, 127, 237)",
    "rgb(127, 51, 0)",
    "rgb(0, 127, 14)",
    "rgb(0, 38, 255)",
]


def create_figure(labels, values, title):
    """Create the donut."""

    fig = go.Figure(
        data=[
            go.Pie(
                title=dict(text=title),
                labels=labels,
                values=values,
                hole=0.5,
                marker_colors=profile_colors,
                marker_line=dict(color="white", width=2),
            )
        ]
    )

    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.2))

    return fig


def code_volume_breakdown(metrics):
    """Determine the code volume."""

    labels = ["Blank Lines", "Lines of Code", "Comment Lines"]
    values = [
        metrics["production"]["SUM"]["blank"],
        metrics["production"]["SUM"]["code"],
        metrics["production"]["SUM"]["comment"],
    ]

    return create_figure(labels, values, "Code breakdown")


def code_type_breakdown(metrics):
    """Determine the code type."""

    labels = ["Production", "Test", "Third Party", "Generated"]
    values = [
        metrics["production"]["SUM"]["code"],
        metrics["test"]["SUM"]["code"],
        metrics["third_party"]["SUM"]["code"],
        metrics["generated"]["SUM"]["code"],
    ]

    return create_figure(labels, values, "Code type <br> breakdown")


def code_breakdown():
    """Show the code break down."""

    settings = {
        "report_directory": "D:\\\\Projects\\github\\sqatt\\reports",
        "analysis_directory": "D:\\\\Projects\\github\\sqatt",
        "code_type": ["production", "test", "third_party", "generated"],
        "production_filter": "--exclude-dir=test,tst,jira,resharper",
        "test_filter": "--match-d=(test|tst)",
        "third_party_filter": "--match-d=(external|ext|jira)",
        "generated_filter": "--match-d=(generated|gen|resharper)",
    }

    metrics = analyze_size(settings)
    container = html.Div(
        [
            html.H3("Code type breakdown"),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="code_type", figure=code_type_breakdown(metrics))),
                ]
            ),
            html.H3("Code breakdown"),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="code_volume", figure=code_volume_breakdown(metrics))),
                ]
            ),
        ]
    )
    return container
