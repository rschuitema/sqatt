"""Create a fan-out profile of the codebase."""

import os
import understand

from src.profile.sqatt_profiles import create_fan_out_profile
from src.reporting.reporting import create_report_directory


def determine_fan_out_profile(profile, database):
    """Determine the fan-in profile."""

    for func in database.ents("function,method,procedure"):
        function_metrics = func.metric(["CountLineCode", "CountOutput"])
        function_size = function_metrics["CountLineCode"]
        function_fan_out = function_metrics["CountOutput"]
        if function_fan_out and function_size:
            profile.update(function_fan_out, function_size)

    return profile


def analyze_fan_out(database, output):
    """Analyze the fan-out."""

    print("Analyzing fan-out.")

    profile = create_fan_out_profile()
    understand_database = understand.open(database)
    profile = determine_fan_out_profile(profile, understand_database)

    profile.print()

    report_file = os.path.join(create_report_directory(output), "fan-out.csv")
    profile.save(report_file)
