"""Header definition of the code quality report."""

from dash import html


def header():
    """Show the header of the code quality report."""

    return html.Div(
        [
            html.H1("Code Quality Report"),
            html.Hr(),
            html.Div(["Auditor: Robbert Schuitema", html.Br(), "Project: Sqatt", html.Br(), "Date: 1-1-2021"]),
        ]
    )
