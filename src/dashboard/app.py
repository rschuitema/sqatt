"""Dash board application to show the code quality report."""

import dash
import dash_bootstrap_components as dbc

from src.dashboard.code_breakdown import code_breakdown
from src.dashboard.code_duplication import code_duplication
from src.dashboard.file_size import file_size_metrics
from src.dashboard.function_metrics import function_metrics
from src.dashboard.header import header
from src.dashboard.language_breakdown import language_breakdown

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container(
    [header(), language_breakdown(), code_breakdown(), code_duplication(), function_metrics(), file_size_metrics()],
)

if __name__ == "__main__":
    app.run_server(port=8888, debug=True)
