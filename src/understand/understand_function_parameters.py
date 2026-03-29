"""Create a profile for the interface sizes of a codebase."""

import os
import understand

from src.profile.sqatt_profiles import create_function_parameters_profile
from src.reporting.reporting import create_report_directory


def determine_function_parameters_profile(profile, database):
    """Determine the function parameters profile."""

    for func in database.ents("function,method,procedure"):
        number_of_parameters = len(func.parameters().split(","))
        function_metrics = func.metric(["CountLineCode"])
        function_size = function_metrics["CountLineCode"]
        if number_of_parameters and function_size:
            profile.update(number_of_parameters, function_size)

    return profile


def analyze_function_parameters(database, output):
    """Analyze the function parameters."""

    print("Analyzing function parameters.")

    profile = create_function_parameters_profile()
    understand_database = understand.open(database)
    profile = determine_function_parameters_profile(profile, understand_database)

    profile.print()

    report_file = os.path.join(create_report_directory(output), "function_parameters.csv")
    profile.save(report_file)
