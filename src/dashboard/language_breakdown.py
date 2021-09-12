"""Show how many languages are used in the project."""

from dash import dcc
from dash import html

from src.cloc.cloc_languages import analyze_languages

from src.profile.colors import profile_colors
from src.profile.show import make_donut


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

    del metrics["SUM"]

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

    return make_donut(labels, values, "Language breakdown", profile_colors)
