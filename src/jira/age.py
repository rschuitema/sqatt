"""Show age report of jira tickets."""

import argparse
from datetime import timedelta, datetime

from bokeh.layouts import row
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange, CustomJS, Div
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

from src.jira.jira_wrapper import login, get_open_defects


class Defect(dict):
    """Represents a jira issue."""

    name = None
    age = None
    status = None
    summary = None

    def __init__(self, name, age, status, summary):
        """Construct the Defect."""

        dict.__init__(self, name=name, age=age, status=status, summary=summary)
        self.name = name
        self.age = age
        self.status = status
        self.summary = summary


def parse_arguments(args):
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")
    parser.add_argument("url", help="The url to the Jira database")
    parser.add_argument("username", help="The Jira username")
    parser.add_argument("password", help="The Jira password")

    return parser.parse_args(args)


def show_defects(sorted_defects, url):
    """Show the defects in a bar graph."""

    output_file("bars.html")

    ages = [">30 days", "20-30 days", "10-20 days", "5-10 days", "<5 days"]
    states = ["New", "Analyzing", "Solving", "Verifying", "Closing", "Postponed"]

    data = count_issues_per_state(sorted_defects, ages)

    x_coordinate = [(age, state) for age in ages for state in states]
    counts = sum(
        zip(
            data["New"],
            data["Analyzing"],
            data["Solving"],
            data["Verifying"],
            data["Closing"],
            data["Postponed"],
        ),
        (),
    )  # like an hstack

    source = ColumnDataSource(data={"x": x_coordinate, "counts": counts})

    plot = create_plot(source, states, x_coordinate)

    div1 = Div()
    # div1 = Div(style={"overflow-y": "scroll", "height": "250px"})
    add_bar_selection_handler(div1, plot, sorted_defects, source, url)

    show(row(plot, div1))


def add_bar_selection_handler(div1, plot, sorted_defects, source, url):
    """Add handler for selecting a bar on the plot."""

    json_issues = convert_age_into_string(sorted_defects)
    on_bar_selected = create_bar_selected_handler(div1, json_issues, source, url)
    plot.js_on_event("tap", on_bar_selected)


def create_plot(source, states, x_coordinate):
    """Create the bar chart."""

    palette = ["#c9d9d3", "#718dbf", "#e84d60", "#111111", "#B200FF", "#7F92FF"]
    plot = figure(
        x_range=FactorRange(*x_coordinate),
        plot_height=250,
        plot_width=1000,
        title="Number of issues per state per age group",
        toolbar_location=None,
        tools=["hover", "tap"],
        tooltips="@counts",
    )
    plot.vbar(x="x", top="counts", width=0.9, source=source)
    plot.vbar(
        x="x",
        top="counts",
        width=0.9,
        source=source,
        line_color="white",
        fill_color=factor_cmap("x", palette=palette, factors=states, start=1, end=2),
    )
    plot.y_range.start = 0
    plot.x_range.range_padding = 0.1
    plot.xaxis.major_label_orientation = 1
    plot.xgrid.grid_line_color = None
    return plot


def create_bar_selected_handler(div1, json_issues, source, url):
    """Handle the bar selection and show the list of issues that belong to the selected bar."""

    on_bar_selected = CustomJS(
        args={"s1": source, "s2": json_issues, "div1": div1, "jira_url": url},
        code="""
        var ind = s1.selected.indices;
        var age_group = s1.data.x[ind][0]
        var state = s1.data.x[ind][1]

        var issues = s2[age_group][state];
        div1.text = 'Issues with status <b>'+ String(state) + '</b> and age <b>' + String(age_group) + '</b><hr>';
        for (i = 0; i < issues.length; i++)
        {
            issue_name = issues[i].name;
            issue_summary = issues[i].summary;
            console.log(`${issue_name} : ${issue_summary}`);
            url = String(jira_url) + "/browse/" + String(issue_name);
            div1.text += `<a href=${url}>${issue_name}</a> : ${issue_summary}<br>`;
        }

        console.log(`${ind}:${age_group}:${state}:${issues.length}`);
    """,
    )
    return on_bar_selected


def convert_age_into_string(sorted_defects):
    """Convert the age field of a Defect into a string."""

    json_issues = sorted_defects
    for buckets in json_issues.values():
        for issues in buckets.values():
            for issue in issues:
                issue.age = str(issue.age)
    return json_issues


def count_issues_per_state(sorted_defects, ages):
    """Count the number of issues per status."""

    data = {
        "New": [0] * 5,
        "Analyzing": [0] * 5,
        "Solving": [0] * 5,
        "Verifying": [0] * 5,
        "Closing": [0] * 5,
        "Postponed": [0] * 5,
        "Age": ages,
    }

    i = 0
    for issues in sorted_defects.values():
        data["New"][i] = len(issues["New"])
        data["Analyzing"][i] = len(issues["Analyzing"])
        data["Solving"][i] = len(issues["Solving"])
        data["Verifying"][i] = len(issues["Verifying"])
        data["Closing"][i] = len(issues["Closing"])
        data["Postponed"][i] = len(issues["Postponed"])
        i += 1

    return data


def get_issue_age(issue):
    """Get the age of an issue."""

    issue_creation_date = datetime.fromisoformat(issue.fields.created.split("+", 1)[0])
    issue_age = datetime.now() - issue_creation_date
    return issue_age


def convert_defects(open_defects):
    """Convert to bokeh structure."""

    issues = []
    for issue in open_defects:
        issue_age = get_issue_age(issue)
        issue_id = issue.key
        issue_status = issue.fields.status.name
        issue_summary = issue.fields.summary
        issues.append(Defect(issue_id, issue_age, issue_status, issue_summary))
    return issues


def sort_defects_on_age(defects):
    """Sort the defects one age group."""

    age_buckets = {
        ">30 days": [],
        "20-30 days": [],
        "10-20 days": [],
        "5-10 days": [],
        "<5 days": [],
    }

    for issue in defects:
        if issue.age > timedelta(days=30):
            age_buckets[">30 days"].append(issue)
        elif issue.age > timedelta(days=20):
            age_buckets["20-30 days"].append(issue)
        elif issue.age > timedelta(days=10):
            age_buckets["10-20 days"].append(issue)
        elif issue.age > timedelta(days=5):
            age_buckets["5-10 days"].append(issue)
        else:
            age_buckets["<5 days"].append(issue)

    return age_buckets


def sort_defects_on_status(defects):
    """Sort the defects on status."""

    new_bucket = ["New", "To Do"]
    analyzing_bucket = ["Analyzing", "To_Analyzing"]
    solving_bucket = ["Solving", "Analyzing_done", "To_Solving"]
    verifying_bucket = ["Verifying", "To_Reviewing", "Reviewing", "To_Verifying"]
    closing_bucket = ["Closing", "Reviewing_Done", "Verifying_Done"]
    postponed_bucket = ["Postponed", "Blocked"]

    buckets = [
        new_bucket,
        analyzing_bucket,
        solving_bucket,
        verifying_bucket,
        closing_bucket,
        postponed_bucket,
    ]

    status_buckets = {
        "New": [],
        "Analyzing": [],
        "Solving": [],
        "Verifying": [],
        "Closing": [],
        "Postponed": [],
    }

    for issue in defects:
        for bucket in buckets:
            if issue.status in bucket:
                status_buckets[bucket[0]].append(issue)

    return status_buckets


def sort_defects_on_status_per_age(defects):
    """Sort the defects on status per age group."""

    age_buckets = {
        ">30 days": [],
        "20-30 days": [],
        "10-20 days": [],
        "5-10 days": [],
        "<5 days": [],
    }

    for bucket, issues in defects.items():
        status_buckets = sort_defects_on_status(issues)
        age_buckets[bucket] = status_buckets

    return age_buckets


def analyze_issue_age(url, username, password):
    """Start of the program."""

    jira = login(url, username, password)

    open_defects = get_open_defects(jira)
    defects = convert_defects(open_defects)

    sorted_defects = sort_defects_on_age(defects)
    sorted_defects = sort_defects_on_status_per_age(sorted_defects)

    show_defects(sorted_defects, url)
