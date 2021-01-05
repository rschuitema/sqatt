"""Create a profile for the function size of the code base."""

import os
import understand

from src.profile.sqatt_profiles import create_function_size_profile
from src.reporting.reporting import create_report_directory


def determine_function_size_profile(profile, understand_database):
    """Determine the function size profile."""

    for func in understand_database.ents("function,method,procedure"):
        function_metrics = func.metric(["CountLineCode"])
        function_size = function_metrics["CountLineCode"]

        if function_size:
            profile.update_loc(function_size)

    return profile


def analyze_function_size(database, output):
    """Analyze the function size."""

    print("Analyzing function size.")

    profile = create_function_size_profile()
    understand_database = understand.open(database)
    profile = determine_function_size_profile(profile, understand_database)

    profile.print()

    report_file = os.path.join(create_report_directory(output), "function_size.csv")
    profile.save(report_file)
