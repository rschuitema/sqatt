"""Create a profile for the function size of the code base."""

import csv
import os
import understand

from src.profile.MetricProfile import MetricProfile
from src.profile.MetricRegion import MetricRegion
from src.understand.understand_report import create_report_directory


def determine_function_size_profile(profile, understand_database):
    """Determine the function size profile."""

    for func in understand_database.ents("function,method,procedure"):
        function_metrics = func.metric(["CountLineCode"])
        function_size = function_metrics["CountLineCode"]

        if function_size:
            profile.update_loc(function_size)

    return profile


def save_function_size_profile(profile, report_file):
    """Save the function size profile to a csv file."""

    with open(report_file, "w") as output:
        csvwriter = csv.writer(
            output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL
        )
        csvwriter.writerow([profile.name(), "Lines Of Code"])
        for region in profile.regions():
            csvwriter.writerow([region.label(), region.loc()])


def analyze_function_size(database, output):
    """Analyze the function size."""

    print("Analyzing function size.")

    regions = [
        MetricRegion("0-15", 0, 16),
        MetricRegion("16-30", 15, 31),
        MetricRegion("31-60", 30, 61),
        MetricRegion("60+", 60, 1001),
    ]

    profile = MetricProfile("Function size", regions)

    understand_database = understand.open(database)
    profile = determine_function_size_profile(profile, understand_database)

    profile.print()

    report_file = os.path.join(create_report_directory(output), "function_size.csv")
    save_function_size_profile(profile, report_file)
