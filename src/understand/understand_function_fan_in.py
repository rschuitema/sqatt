"""Create a fan-in profile of the codebase."""

import csv
import os
import understand

from src.profile.MetricProfile import MetricProfile
from src.profile.MetricRegion import MetricRegion
from src.understand.understand_report import create_report_directory


def determine_fan_in_profile(profile, database):
    """Determine the fan-in profile."""

    for func in database.ents("function,method,procedure"):
        function_metrics = func.metric(["CountLineCode", "CountInput"])
        function_size = function_metrics["CountLineCode"]
        function_fan_in = function_metrics["CountInput"]
        if function_fan_in and function_size:
            profile.update(function_fan_in, function_size)

    return profile


def save_fan_in_profile(profile, report_file):
    """Save the fan-in profile to a csv file."""

    with open(report_file, "w") as output:
        csvwriter = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)
        csvwriter.writerow([profile.name(), "Lines Of Code"])
        for region in profile.regions():
            csvwriter.writerow([region.label(), region.loc()])


def analyze_fan_in(database, output):
    """Analyze the fan-in."""

    print("Analyzing fan-in.")

    regions = [
        MetricRegion("1-10", 1, 10),
        MetricRegion("11-20", 11, 20),
        MetricRegion("21-50", 21, 50),
        MetricRegion("50+", 51, 1001),
    ]

    profile = MetricProfile("Fan-in", regions)
    understand_database = understand.open(database)
    profile = determine_fan_in_profile(profile, understand_database)

    profile.print()

    report_file = os.path.join(create_report_directory(output), "fan-in.csv")
    save_fan_in_profile(profile, report_file)
