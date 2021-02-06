"""Show the code duplication metric."""

import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go

from src.cpd.cpd_analysis import analyze_duplication


def determine_colors(percentage):
    """
    Determine the color of the duplicated section.

    The color depends on the amount of code duplication.
    """

    colors = []

    if 3 >= percentage > 0:
        colors.append("rgb(121, 185, 79)")
    elif 5 >= percentage > 3:
        colors.append("rgb(255, 204, 5)")
    elif 20 >= percentage > 5:
        colors.append("rgb(251, 135, 56)")
    else:
        colors.append("rgb(204, 5, 5)")

    colors.append("rgb(121, 185, 79)")

    return colors


def create_figure(labels, values, colors, title):
    """Create the donut."""

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


def code_duplication():
    """Determine the code duplication."""

    settings = {
        "report_directory": "D:\\\\Projects\\github\\sqatt\\reports",
        "analysis_directory": "D:\\\\Projects\\github\\sqatt",
        "tokens": "20",
        "language": "python",
    }

    metrics = analyze_duplication(settings)

    content = html.Div(
        [html.H3("Code duplication"), dcc.Graph(id="code_duplication", figure=code_duplication_figure(metrics))],
    )
    return content


def code_duplication_figure(metrics):
    """Create the code duplication donut."""

    duplicated_loc = metrics["duplicated_loc"]
    total_loc = metrics["total_loc"]

    labels = ["Duplicated code", "Non duplicated code"]
    values = [duplicated_loc, (total_loc - duplicated_loc)]

    percentage = (duplicated_loc / total_loc) * 100

    colors = determine_colors(percentage)

    return create_figure(labels, values, colors, "Code duplication")
