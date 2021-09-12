"""Show the function metrics: complexity, function size and function parameters."""

from dash import dcc
from dash import html

from src.lizard.lizard_analysis import measure_function_metrics, create_profiles, determine_profiles
from src.profile.show import make_profile


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
            dcc.Graph(id="complexity", figure=make_profile(profiles["complexity"])),
            html.H3("Function size"),
            dcc.Graph(id="function_size", figure=make_profile(profiles["function_size"])),
            html.H3("Function parameters"),
            dcc.Graph(id="function_parameters", figure=make_profile(profiles["parameters"])),
        ]
    )
    return container
