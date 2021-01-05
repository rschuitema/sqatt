"""Create a profile of the complexity of the codebase."""

import os
import understand

from src.profile.sqatt_profiles import create_complexity_profile
from src.reporting.reporting import create_report_directory


def determine_complexity_profile(profile, database):
    """Determine the complexity profile."""

    for func in database.ents("function,method,procedure"):
        function_metrics = func.metric(["CountLineCode", "Cyclomatic"])
        function_size = function_metrics["CountLineCode"]
        function_complexity = function_metrics["Cyclomatic"]
        if function_complexity and function_size:
            profile.update(function_complexity, function_size)

    return profile


def analyze_complexity(database, output):
    """Analyze the complexity."""

    print("Analyzing complexity.")

    profile = create_complexity_profile()
    understand_database = understand.open(database)
    profile = determine_complexity_profile(profile, understand_database)

    profile.print()

    report_file = os.path.join(create_report_directory(output), "fan-in.csv")
    profile.save(report_file)
