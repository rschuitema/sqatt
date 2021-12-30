"""Show the profile in a donut."""

import plotly.graph_objects as go

from src.profile.colors import PROFILE_COLORS


def make_donut(labels, values, title, colors):
    """Show the values in a donut."""

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


def make_profile(profile):
    """Make the profile."""
    labels = []
    values = []
    for region in profile.regions():
        labels.append(region.label())
        values.append(region.loc())

    fig = make_donut(labels, values, profile.name(), PROFILE_COLORS)
    return fig


def show_profile(profile):
    """Show the profile in a donut."""

    fig = make_profile(profile)
    fig.show()
