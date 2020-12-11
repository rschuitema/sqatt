"""Create a profile for the interface sizes of a codebase."""

import csv
import os
import understand

from src.profile.MetricProfile import MetricProfile
from src.profile.MetricRegion import MetricRegion
from src.understand.understand_report import create_report_directory


def determine_function_parameters_profile(profile, database):
    """Determine the function parameters profile."""

    for func in database.ents("function,method,procedure"):
        number_of_parameters = len(func.parameters().split(","))
        function_metrics = func.metric(["CountLineCode"])
        function_size = function_metrics["CountLineCode"]
        if number_of_parameters and function_size:
            profile.update(number_of_parameters, function_size)

    return profile


def save_function_parameters_profile(profile, report_file):
    """Save the function parameters profile to a csv file."""

    with open(report_file, "w") as output:
        csvwriter = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)
        csvwriter.writerow([profile.name(), "Lines Of Code"])
        for region in profile.regions():
            csvwriter.writerow([region.label(), region.loc()])


def analyze_function_parameters(database, output):
    """Analyze the function parameters."""

    print("Analyzing function parameters.")

    regions = [
        MetricRegion("1-2", 1, 2),
        MetricRegion("3-4", 3, 4),
        MetricRegion("5-6", 5, 6),
        MetricRegion("6+", 6, 10),
    ]

    profile = MetricProfile("Fan-in", regions)
    understand_database = understand.open(database)
    profile = determine_function_parameters_profile(profile, understand_database)

    profile.print()

    report_file = os.path.join(create_report_directory(output), "function_parameters.csv")
    save_function_parameters_profile(profile, report_file)
