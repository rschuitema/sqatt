"""Create different profiles of resharper issues."""

import argparse
import csv
import json
import os

import xmltodict
from defusedxml import ElementTree
import plotly.graph_objects as go

from src.reporting.reporting import create_report_directory


def parse_arguments():
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("issuefile", help="resharper issue file to parse")
    parser.add_argument("--reportdir", help="directory where to place the report")
    args = parser.parse_args()
    return args


def read_resharper_issues(filename):
    """Read the resharper issues into a dictionary."""

    with open(filename, encoding="utf-8") as input_file:
        doc = xmltodict.parse(input_file.read())

    return doc


def determine_issue_types(warnings):
    """
    Get a list of issue types.

    :rtype: list
    """

    issue_types = warnings["Report"]["IssueTypes"]["IssueType"]
    if not isinstance(issue_types, list):
        return [issue_types]
    return issue_types


def determine_projects(warnings):
    """
    Get the list of projects.

    :rtype: list
    """

    projects = warnings["Report"]["Issues"]["Project"]
    if not isinstance(projects, list):
        return [projects]
    return projects


def determine_issues(project):
    """
    Get the list of issues of a project.

    :rtype: list
    """

    issues = project["Issue"]
    if not isinstance(issues, list):
        return [issues]
    return issues


def determine_issue_category(issue_type, issue_types):
    """Determine the category of an issue."""

    category = None
    for issue in issue_types:
        issue_id = issue["@Id"]
        if issue_id == issue_type:
            category = issue["@Category"]
            break

    return category


def increment_issue_count_for_category(issue, issue_types, issues_per_category):
    """Increment the issue count for a category."""

    issue_type = issue["@TypeId"]
    issue_category = determine_issue_category(issue_type, issue_types)
    increment_issue_count(issue_category, issues_per_category)


def increment_issue_count_for_issue_types(issue, issues_per_issue_type):
    """Increment the issue count for issue types."""

    issue_type = issue["@TypeId"]
    increment_issue_count(issue_type, issues_per_issue_type)


def increment_issue_count(item, item_dict):
    """Increment the issue count of an item in a dictionary."""

    if item in item_dict:
        item_dict[item] += 1
    else:
        item_dict[item] = 1


def determine_issues_per_project(warnings):
    """Create the issues per project profile."""

    issues_per_project = {}

    projects = determine_projects(warnings)

    for project in projects:
        issues = determine_issues(project)
        issues_per_project[project["@Name"]] = len(issues)

    return issues_per_project


def determine_issues_per_issuetype(warnings):
    """Create the issues per issue type profile."""

    issues_per_issue_type = {}
    projects = determine_projects(warnings)
    for project in projects:
        issues = determine_issues(project)
        for issue in issues:
            increment_issue_count_for_issue_types(issue, issues_per_issue_type)

    return issues_per_issue_type


def determine_issues_per_category(warnings):
    """Create the issues per category profile."""

    issues_per_category = {}
    issue_types = determine_issue_types(warnings)

    projects = determine_projects(warnings)
    for project in projects:
        issues = determine_issues(project)
        for issue in issues:
            increment_issue_count_for_category(issue, issue_types, issues_per_category)

    return issues_per_category


def save_issues(item_dict, report_file, item_name="Item"):
    """Save the issues in a csv file."""

    with open(report_file, "w", encoding="utf-8") as output:
        csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)
        csv_writer.writerow([item_name, "Number of violations"])
        for item in item_dict:
            csv_writer.writerow([item, item_dict[item]])


def save_issues_per_project(issues_per_project, report_dir):
    """Save the issues per project profile."""

    report_file = os.path.join(report_dir, "issues_per_project.csv")
    save_issues(issues_per_project, report_file, "Project")


def save_issues_per_issue_type(issues_per_issue_type, report_dir):
    """Save the issues per issue type profile."""

    report_file = os.path.join(report_dir, "issues_per_issue_type.csv")
    save_issues(issues_per_issue_type, report_file, "Issue Type")


def save_issues_per_category(issues_per_category, report_dir):
    """Save the issues per category profile."""

    report_file = os.path.join(report_dir, "issues_per_category.csv")
    save_issues(issues_per_category, report_file, "Category")


def save_as_json(warnings):
    """Save the resharper output in json format."""

    with open("resharper_results.json", "w", encoding="utf-8") as outfile:
        json.dump(warnings, outfile, indent=4)


def filter_out(filename, tmp_filename):
    """Filter out generated code and Dezyne code."""

    with open(filename, "r", encoding="utf-8") as input_file:
        doc = ElementTree.parse(input_file)
        for elem in doc.xpath("//*/Project"):
            if "Proxy" in elem.attrib["Name"]:
                parent = elem.getparent()
                parent.remove(elem)
            if "Dezyne" in elem.attrib["Name"]:
                parent = elem.getparent()
                parent.remove(elem)
        print(ElementTree.tostring(doc))
        with open(tmp_filename, "w", encoding="utf-8") as tmp_file:
            tmp_file.write(str(ElementTree.tostring(doc, encoding="unicode")))


def show_issues_per_project(issues_per_project):
    """Show the issues per project in a bar graph."""

    x_axis = []
    y_axis = []
    for item in issues_per_project:
        x_axis.append(item)
        y_axis.append(issues_per_project[item])

    fig = go.Figure([go.Bar(x=x_axis, y=y_axis)])
    fig.update_layout(title_text="Violations per project", yaxis={"title": "Number of violations"})
    fig.show()


def main():
    """Start of the program."""

    args = parse_arguments()

    filename = args.issuefile

    # pre, ext = os.path.splitext(filename)
    # ext = ext.replace("xml", "tmp")
    # tmp_filename = pre + ext

    # filter_out(filename, tmp_filename)
    warnings = read_resharper_issues(filename)
    # os.remove(tmp_filename)

    issues_per_project = determine_issues_per_project(warnings)
    issues_per_issue_type = determine_issues_per_issuetype(warnings)
    issues_per_category = determine_issues_per_category(warnings)

    report_dir = create_report_directory(args.reportdir)

    save_issues_per_project(issues_per_project, report_dir)
    save_issues_per_issue_type(issues_per_issue_type, report_dir)
    save_issues_per_category(issues_per_category, report_dir)

    save_as_json(warnings)

    show_issues_per_project(issues_per_project)


if __name__ == "__main__":
    main()
