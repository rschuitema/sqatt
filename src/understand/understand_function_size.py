"""Create a profile for the function size of the code base."""

import argparse
import csv
import os
import understand


class FunctionSizeProfile:
    """Profile of the function size."""

    def __init__(self):
        self.function_size_green = 0
        self.function_size_yellow = 0
        self.function_size_orange = 0
        self.function_size_red = 0
        self.total_lines_of_code = 0

    def add_function_size(self, size):
        """Add the function size to update the profile."""

        self.total_lines_of_code = self.total_lines_of_code + size
        if size <= 15:
            self.function_size_green = self.function_size_green + size
        elif size <= 30:
            self.function_size_yellow = self.function_size_yellow + size
        elif size <= 60:
            self.function_size_orange = self.function_size_orange + size
        else:
            self.function_size_red = self.function_size_red + size

    def get_total_lines_of_code(self):
        """Return the total lines of code that is written in functions."""

        return self.total_lines_of_code


def parse_arguments():
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("database", help="understand database to parse")
    parser.add_argument("--reportdir", help="directory where to place the report")
    args = parser.parse_args()
    return args


def create_report_directory(directory):
    """Create the report directory."""

    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def determine_function_size_profile(profile, understand_database):
    """Determine the function size profile."""

    for func in understand_database.ents("function,method,procedure"):
        function_metrics = func.metric(["CountLineBlank",
                                        "CountLineCode",
                                        "CountLineComment",
                                        "CountLineInactive",
                                        "Cyclomatic",
                                        "CountInput",
                                        "CountOutput"])

        function_size = function_metrics["CountLineCode"]

        if function_size:
            profile.add_function_size(function_size)

    return profile


def print_profile(profile):
    """Print the profile."""

    print("green function size :", profile.function_size_green)
    print("yellow function size :", profile.function_size_yellow)
    print("orange function size :", profile.function_size_orange)
    print("red function size :", profile.function_size_red)
    print("lines of code in functions :", profile.total_lines_of_code)


def save_function_size_profile(profile, report_file):
    """Save the function size profile to a csv file"""

    with open(report_file, 'w') as output:
        csvwriter = csv.writer(output, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL)
        csvwriter.writerow(['Function size', 'Lines Of Code'])
        csvwriter.writerow(["1-15", profile.function_size_green])
        csvwriter.writerow(["16-30", profile.function_size_yellow])
        csvwriter.writerow(["31-60", profile.function_size_orange])
        csvwriter.writerow(["61+", profile.function_size_red])


def main():
    """The entry point of the program."""

    args = parse_arguments()
    understand_database = understand.open(args.database)

    profile = FunctionSizeProfile()

    profile = determine_function_size_profile(profile, understand_database)

    print_profile(profile)

    report_file = os.path.join(create_report_directory(args.reportdir), "function_size.csv")
    save_function_size_profile(profile, report_file)


if __name__ == "__main__":
    main()
