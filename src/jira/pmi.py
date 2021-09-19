"""Calculate the pondered maturity index for defects."""

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Div
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.io import output_file, show

from src.jira.jira_wrapper import login, get_open_defects


ANALYZING_FACTORS = {
    "Severe": {"Factor": 80, "Count": 0, "Defects": []},
    "Critical": {"Factor": 40, "Count": 0, "Defects": []},
    "Major": {"Factor": 20, "Count": 0, "Defects": []},
    "Minor": {"Factor": 0, "Count": 0, "Defects": []},
    "Trivial": {"Factor": 0, "Count": 0, "Defects": []},
}

SOLVING_FACTORS = {
    "Severe": {"Factor": 60, "Count": 0, "Defects": []},
    "Critical": {"Factor": 30, "Count": 0, "Defects": []},
    "Major": {"Factor": 15, "Count": 0, "Defects": []},
    "Minor": {"Factor": 0, "Count": 0, "Defects": []},
    "Trivial": {"Factor": 0, "Count": 0, "Defects": []},
}

VERIFYING_FACTORS = {
    "Severe": {"Factor": 40, "Count": 0, "Defects": []},
    "Critical": {"Factor": 20, "Count": 0, "Defects": []},
    "Major": {"Factor": 10, "Count": 0, "Defects": []},
    "Minor": {"Factor": 0, "Count": 0, "Defects": []},
    "Trivial": {"Factor": 0, "Count": 0, "Defects": []},
}

CLOSING_FACTORS = {
    "Severe": {"Factor": 20, "Count": 0, "Defects": []},
    "Critical": {"Factor": 10, "Count": 0, "Defects": []},
    "Major": {"Factor": 5, "Count": 0, "Defects": []},
    "Minor": {"Factor": 0, "Count": 0, "Defects": []},
    "Trivial": {"Factor": 0, "Count": 0, "Defects": []},
}

POSTPONED_FACTORS = {
    "Severe": {"Factor": 0, "Count": 0, "Defects": []},
    "Critical": {"Factor": 0, "Count": 0, "Defects": []},
    "Major": {"Factor": 0, "Count": 0, "Defects": []},
    "Minor": {"Factor": 0, "Count": 0, "Defects": []},
    "Trivial": {"Factor": 0, "Count": 0, "Defects": []},
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
    "Closing": CLOSING_FACTORS,
    "Postponed": POSTPONED_FACTORS,
    "Blocked": POSTPONED_FACTORS,
}


def create_cell_selected_handler(div1, data_source, url):
    """Handle the bar selection and show the list of issues that belong to the selected bar."""

    source_code = """
        var ind = s1.selected.indices;

        var status = s1.data.status[ind];
        var grid = document.getElementsByClassName('grid-canvas')[0].children;
        var column = 0;

        for (var j = 0, jmax = grid[ind].children.length; j < jmax; j++)
            if(grid[ind].children[j].outerHTML.includes('active'))
                { column = j }

        var col = s1.data.severity[column-1];
        console.log(`status:${status} col:${col} column:${column}`);

        var issues = s2[status][col]["Defects"];

        console.log(`issues:${issues} :${issues.length}`);

        div1.text = 'Issues with status <b>'+ String(status) + '</b> and severity <b>' + String(col) + '</b><hr>';
        for (i = 0; i < issues.length; i++)
        {
            issue_name = issues[i][0];
            issue_summary = issues[i][1];
            console.log(`${issue_name} : ${issue_summary}`);
            url = String(jira_url) + "/browse/" + String(issue_name);
            div1.text += `<a href=${url}>${issue_name}</a> : ${issue_summary}<br>`;
        }
    """
    on_cell_selected = CustomJS(
        args=dict(s1=data_source, s2=PMI_FACTORS, div1=div1, jira_url=url),
        code=source_code,
    )

    return on_cell_selected


def calculate_pmi(open_defects):
    """Calculate the PMI."""

    pmi = 0
    for issue in open_defects:
        issue_status = issue.fields.status.name
        issue_severity = "Severe"

        if issue_status in PMI_FACTORS:
            PMI_FACTORS[issue_status][issue_severity]["Count"] += 1
            PMI_FACTORS[issue_status][issue_severity]["Defects"].append((issue.key, issue.fields.summary))
            pmi += PMI_FACTORS[issue_status][issue_severity]["Factor"]

    return pmi


def show_pmi(pmi, url):
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
        severity=["Severe", "Critical", "Major", "Minor", "Trivial"],
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

    data_table = DataTable(
        source=source,
        columns=columns,
        width=400,
        height=280,
        index_position=None,
        sortable=False,
    )

    issue_div = Div()
    callback = create_cell_selected_handler(issue_div, source, url)

    # pylint: disable=E1101
    source.selected.js_on_change("indices", callback)
    # pylint: enable=E1101

    pmi_div = Div(text=f"PMI: {pmi}")
    show(row(column(data_table, pmi_div), issue_div))


def analyze_pmi(url, username, password):
    """Analyze the PMI."""

    jira = login(url, username, password)
    open_defects = get_open_defects(jira)

    pmi = calculate_pmi(open_defects)
    show_pmi(pmi, url)
