"""Show the profile in a donut."""

import plotly.graph_objects as go

from src.profile.colors import profile_colors


def profile_figure(profile):
    """Create the profile donut."""

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


def show_profile(profile):
    """Show the profile in a donut."""

    fig = profile_figure(profile)
    fig.show()
