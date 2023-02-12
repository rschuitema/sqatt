"""Overview of the quality in a radar chart."""

import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go


def overview():
    """Create an overview of the metrics in a radar chart."""

    content = html.Div(
        [html.H3("Rating"), dcc.Graph(id="rating", figure=overview_graph())],
    )
    return content


def overview_graph():
    """Create the radar chart."""

    fig = go.Figure(
        data=go.Scatterpolar(
            r=[1, 5, 2, 2, 3],
            theta=["Code duplication", "Complexity", "Function size", "Dependencies", "Fan-in", "Fan-out"],
            fill="toself",
        )
    )

    fig.update_layout(
        polar={"radialaxis": {"visible": True}},
        showlegend=False,
    )
    fig.update_layout(legend={"orientation": 'h', "yanchor": 'bottom', "xanchor": 'center', "x": 0.5})

    return fig
