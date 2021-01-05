"""Create a fan-in profile of the codebase."""

import os
import understand

from src.profile.sqatt_profiles import create_fan_in_profile
from src.reporting.reporting import create_report_directory


def determine_fan_in_profile(profile, database):
    """Determine the fan-in profile."""

    for func in database.ents("function,method,procedure"):
        function_metrics = func.metric(["CountLineCode", "CountInput"])
        function_size = function_metrics["CountLineCode"]
        function_fan_in = function_metrics["CountInput"]
        if function_fan_in and function_size:
            profile.update(function_fan_in, function_size)

    return profile


def analyze_fan_in(database, output):
    """Analyze the fan-in."""

    print("Analyzing fan-in.")

    profile = create_fan_in_profile()
    understand_database = understand.open(database)
    profile = determine_fan_in_profile(profile, understand_database)

    profile.print()

    report_file = os.path.join(create_report_directory(output), "fan-in.csv")
    profile.save(report_file)
