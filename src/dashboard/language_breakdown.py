"""Show how many languages are used in the project."""

import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go

from src.cloc.cloc_languages import analyze_languages

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
    """Create the donut to show the metric."""

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


def language_breakdown():
    """Create the language break down."""

    settings = {
        "report_directory": "D:\\\\Projects\\github\\sqatt\\reports",
        "analysis_directory": "D:\\\\Projects\\github\\sqatt",
        "code_type": ["production", "test", "third_party", "generated"],
        "production_filter": "--exclude-dir=test,tst,jira,resharper",
        "test_filter": "--match-d=(test|tst)",
        "third_party_filter": "--match-d=(external|ext|jira)",
        "generated_filter": "--match-d=(generated|gen|resharper)",
    }

    metrics = analyze_languages(settings)

    content = html.Div(
        [html.H3("Language breakdown"), dcc.Graph(id="language_breakdown", figure=language_breakdown_figure(metrics))],
    )
    return content


def language_breakdown_figure(metrics):
    """Create the figure to show the language break down."""

    labels = []
    values = []
    for language, metric in metrics.items():
        labels.append(language)
        values.append(metric["code"])

    return create_figure(labels, values, "Language breakdown")
