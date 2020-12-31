"""Create a profile for the function size of the code base."""
import csv
import os

from src.facility.subprocess import Subprocess
from src.profile.MetricProfile import MetricProfile
from src.profile.MetricRegion import MetricRegion
from src.reporting.reporting import create_report_directory


def determine_function_size_profile(profile, report_file, reader=None):
    """Determine the profile for the function size."""

    with open(report_file, "r", newline="\n") as csv_file:
        csv_reader = reader or csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            profile.update_loc(int(row[0]))


def analyze_function_size(input_dir, output_dir):
    """Analyze the function size."""

    report_dir = create_report_directory(output_dir)
    function_size_file = os.path.join(report_dir, "function_size.csv")

    measure_function_size(input_dir, function_size_file)

    regions = [
        MetricRegion("0-15", 0, 16),
        MetricRegion("16-30", 15, 31),
        MetricRegion("31-60", 30, 61),
        MetricRegion("60+", 60, 1001),
    ]

    profile = MetricProfile("Function size", regions)

    determine_function_size_profile(profile, function_size_file)

    profile.print()

    function_size_profile_file = os.path.join(report_dir, "function_size_profile.csv")
    profile.save(function_size_profile_file)


def measure_function_size(input_dir, report_file):
    """Measure the function size."""

    measure_function_size_command = [
        "lizard",
        "--csv",
        f"-o{report_file}",
        input_dir,
    ]

    process = Subprocess(measure_function_size_command, verbose=3)
    process.execute()
