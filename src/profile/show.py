"""Show the profile in a donut."""

import plotly.graph_objects as go

profile_colors = [
    "rgb(121, 185, 79)",
    "rgb(255, 204, 5)",
    "rgb(251, 135, 56)",
    "rgb(204, 5, 5)",
    "rgb(121,55,171)",
    "rgb(255, 127, 237)",
    "rgb(127, 51, 0)",
    "rgb(0, 127, 14)",
    "rgb(0, 38, 255)",
]


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

    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5))

    return fig


def show_profile(profile):
    """Show the profile in a donut."""

    fig = profile_figure(profile)
    fig.show()
