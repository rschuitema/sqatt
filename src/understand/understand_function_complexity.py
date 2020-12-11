"""Create a profile of the complexity of the codebase."""

import csv
import os
import understand

from src.profile.MetricProfile import MetricProfile
from src.profile.MetricRegion import MetricRegion
from src.understand.understand_report import create_report_directory


def determine_complexity_profile(profile, database):
    """Determine the complexity profile."""

    for func in database.ents("function,method,procedure"):
        function_metrics = func.metric(["CountLineCode", "Cyclomatic"])
        function_size = function_metrics["CountLineCode"]
        function_complexity = function_metrics["Cyclomatic"]
        if function_complexity and function_size:
            profile.update(function_complexity, function_size)

    return profile


def save_complexity_profile(profile, report_file):
    """Save the complexity profile to a csv file."""

    with open(report_file, "w") as output:
        csvwriter = csv.writer(
            output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL
        )
        csvwriter.writerow([profile.name(), "Lines Of Code"])
        for region in profile.regions():
            csvwriter.writerow([region.label(), region.loc()])


def analyze_complexity(database, output):
    """Analyze the complexity."""

    print("Analyzing complexity.")

    regions = [
        MetricRegion("0-5", 0, 5),
        MetricRegion("6-10", 6, 10),
        MetricRegion("11-25", 11, 25),
        MetricRegion("25+", 26, 1001),
    ]

    profile = MetricProfile("Fan-in", regions)
    understand_database = understand.open(database)
    profile = determine_complexity_profile(profile, understand_database)

    profile.print()

    report_file = os.path.join(create_report_directory(output), "fan-in.csv")
    save_complexity_profile(profile, report_file)
