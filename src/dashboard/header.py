"""Header definition of the code quality report."""

import dash_bootstrap_components as dbc
import dash_html_components as html


def header():
    """Show the header of the code quality report."""

    jumbotron = dbc.Jumbotron(
        [
            html.H1("Code Quality Report"),
            html.Hr(),
            html.Div(["Auditor: Robbert Schuitema", html.Br(), "Project: Sqatt", html.Br(), "Date: 1-1-2021"]),
        ]
    )
    return jumbotron
