"""Calculate the pondered maturity index for defects."""

from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.io import output_file, show

from src.jira.jira_wrapper import login, get_open_defects


ANALYZING_FACTORS = {
    "Severe": {"Factor": 80, "Count": 0},
    "Critical": {"Factor": 40, "Count": 0},
    "Major": {"Factor": 20, "Count": 0},
    "Minor": {"Factor": 0, "Count": 0},
    "Trivial": {"Factor": 0, "Count": 0},
}

SOLVING_FACTORS = {
    "Severe": {"Factor": 60, "Count": 0},
    "Critical": {"Factor": 30, "Count": 0},
    "Major": {"Factor": 15, "Count": 0},
    "Minor": {"Factor": 0, "Count": 0},
    "Trivial": {"Factor": 0, "Count": 0},
}

VERIFYING_FACTORS = {
    "Severe": {"Factor": 40, "Count": 0},
    "Critical": {"Factor": 20, "Count": 0},
    "Major": {"Factor": 10, "Count": 0},
    "Minor": {"Factor": 0, "Count": 0},
    "Trivial": {"Factor": 0, "Count": 0},
}

CLOSING_FACTORS = {
    "Severe": {"Factor": 20, "Count": 0},
    "Critical": {"Factor": 10, "Count": 0},
    "Major": {"Factor": 5, "Count": 0},
    "Minor": {"Factor": 0, "Count": 0},
    "Trivial": {"Factor": 0, "Count": 0},
}

POSTPONED_FACTORS = {
    "Severe": {"Factor": 0, "Count": 0},
    "Critical": {"Factor": 0, "Count": 0},
    "Major": {"Factor": 0, "Count": 0},
    "Minor": {"Factor": 0, "Count": 0},
    "Trivial": {"Factor": 0, "Count": 0},
}

PMI_FACTORS = {
    "New": ANALYZING_FACTORS,
    "To_Do": ANALYZING_FACTORS,
    "To_Analyzing": ANALYZING_FACTORS,
    "Analyzing": ANALYZING_FACTORS,
    "Analyzing_Done": SOLVING_FACTORS,
    "To_Solving": SOLVING_FACTORS,
    "Solving": SOLVING_FACTORS,
    "Solving_Done": VERIFYING_FACTORS,
    "To_Reviewing": VERIFYING_FACTORS,
    "Reviewing": VERIFYING_FACTORS,
    "To_Verifying": VERIFYING_FACTORS,
    "Verifying": VERIFYING_FACTORS,
    "Verifying_Done": CLOSING_FACTORS,
    "Reviewing_Done": CLOSING_FACTORS,
    "Postponed": POSTPONED_FACTORS,
    "Blocked": POSTPONED_FACTORS,
}


def calculate_pmi(url, username, password):
    """Calculate the PMI."""

    jira = login(url, username, password)
    open_defects = get_open_defects(jira)

    pmi = 0
    for issue in open_defects:
        issue_status = issue.fields.status.name
        issue_severity = "Severe"

        if issue_status in PMI_FACTORS.keys():
            PMI_FACTORS[issue_status][issue_severity]["Count"] += 1
            pmi += PMI_FACTORS[issue_status][issue_severity]["Factor"]

    return pmi


def show_pmi():
    """Show the PMI in a table."""

    output_file("data_table.html")

    severe_counts = [0, 0, 0, 0, 0]
    critical_counts = [0, 0, 0, 0, 0]
    major_counts = [0, 0, 0, 0, 0]
    minor_counts = [0, 0, 0, 0, 0]
    trivial_counts = [0, 0, 0, 0, 0]

    severe_counts[0] = ANALYZING_FACTORS["Severe"]["Count"]
    severe_counts[1] = SOLVING_FACTORS["Severe"]["Count"]
    severe_counts[2] = VERIFYING_FACTORS["Severe"]["Count"]
    severe_counts[3] = CLOSING_FACTORS["Severe"]["Count"]
    severe_counts[4] = POSTPONED_FACTORS["Severe"]["Count"]

    critical_counts[0] = ANALYZING_FACTORS["Critical"]["Count"]
    critical_counts[1] = SOLVING_FACTORS["Critical"]["Count"]
    critical_counts[2] = VERIFYING_FACTORS["Critical"]["Count"]
    critical_counts[3] = CLOSING_FACTORS["Critical"]["Count"]
    critical_counts[4] = POSTPONED_FACTORS["Critical"]["Count"]

    major_counts[0] = ANALYZING_FACTORS["Major"]["Count"]
    major_counts[1] = SOLVING_FACTORS["Major"]["Count"]
    major_counts[2] = VERIFYING_FACTORS["Major"]["Count"]
    major_counts[3] = CLOSING_FACTORS["Major"]["Count"]
    major_counts[4] = POSTPONED_FACTORS["Major"]["Count"]

    minor_counts[0] = ANALYZING_FACTORS["Minor"]["Count"]
    minor_counts[1] = SOLVING_FACTORS["Minor"]["Count"]
    minor_counts[2] = VERIFYING_FACTORS["Minor"]["Count"]
    minor_counts[3] = CLOSING_FACTORS["Minor"]["Count"]
    minor_counts[4] = POSTPONED_FACTORS["Minor"]["Count"]

    trivial_counts[0] = ANALYZING_FACTORS["Trivial"]["Count"]
    trivial_counts[1] = SOLVING_FACTORS["Trivial"]["Count"]
    trivial_counts[2] = VERIFYING_FACTORS["Trivial"]["Count"]
    trivial_counts[3] = CLOSING_FACTORS["Trivial"]["Count"]
    trivial_counts[4] = POSTPONED_FACTORS["Trivial"]["Count"]

    data = dict(
        status=["Analyzing", "Solving", "Verifying", "Closing", "Postponed"],
        severe=severe_counts,
        critical=critical_counts,
        major=major_counts,
        minor=minor_counts,
        trivial=trivial_counts,
    )
    source = ColumnDataSource(data)

    columns = [
        TableColumn(field="status", title=""),
        TableColumn(field="severe", title="Severe"),
        TableColumn(field="critical", title="Critical"),
        TableColumn(field="major", title="Major"),
        TableColumn(field="minor", title="Minor"),
        TableColumn(field="trivial", title="Trivial"),
    ]

    data_table = DataTable(source=source, columns=columns, width=400, height=280, index_position=None, sortable=False)
    show(widgetbox(data_table))
