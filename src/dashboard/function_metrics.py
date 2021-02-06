"""Show the function metrics: complexity, function size and function parameters."""

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

from src.lizard.lizard_analysis import measure_function_metrics, create_profiles, determine_profiles


profile_colors = ["rgb(121, 185, 79)", "rgb(255, 204, 5)", "rgb(251, 135, 56)", "rgb(204, 5, 5)", "rgb(121,55,171)"]


def create_figure(profile):
    """Show the profile in a donut."""

    labels = []
    values = []
    for region in profile.regions():
        labels.append(region.label())
        values.append(region.loc())

    fig = go.Figure(
        data=[
            go.Pie(
                title=dict(text=profile.name()),
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


def function_metrics():
    """Determine the function metrics."""

    settings = {
        "report_directory": "D:\\\\Projects\\github\\sqatt\\reports",
        "analysis_directory": "D:\\\\Projects\\github\\sqatt",
        "tokens": "20",
        "language": "python",
    }

    metrics_file = measure_function_metrics(settings["analysis_directory"], settings["report_directory"])
    profiles = create_profiles()
    determine_profiles(profiles, metrics_file)

    container = html.Div(
        [
            html.H3("Complexity"),
            dcc.Graph(id="complexity", figure=create_figure(profiles["complexity"])),
            html.H3("Function size"),
            dcc.Graph(id="function_size", figure=create_figure(profiles["function_size"])),
            html.H3("Function parameters"),
            dcc.Graph(id="function_parameters", figure=create_figure(profiles["parameters"])),
        ]
    )
    return container
