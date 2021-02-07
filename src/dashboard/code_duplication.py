"""Show the code duplication metric."""

import dash_core_components as dcc
import dash_html_components as html

from src.cpd.cpd_analysis import analyze_duplication, determine_colors

from src.profile.show import make_donut


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

    return make_donut(labels, values, "Code duplication", colors)
