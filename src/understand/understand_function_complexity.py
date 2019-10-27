"""Create a profile of the complexity of the codebase."""

import argparse
import csv
import os
import understand

from src.understand.understand_report import create_report_directory


def parse_arguments():
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("database", help="understand database to parse")
    parser.add_argument("--reportdir", help="directory where to place the report")
    args = parser.parse_args()
    return args


def measure_function_complexity(database):
    """Create the complexity profile."""

    function_size_green = 0
    number_of_functions_green = 0
    function_size_yellow = 0
    number_of_functions_yellow = 0
    function_size_orange = 0
    number_of_functions_orange = 0
    function_size_red = 0
    number_of_functions_red = 0

    for func in database.ents("function,method,procedure"):
        function_metrics = func.metric(["CountLineCode", "Cyclomatic"])
        function_size = function_metrics["CountLineCode"]
        function_complexity = function_metrics["Cyclomatic"]

        if function_size:
            if function_complexity <= 5:
                function_size_green = function_size_green + function_size
                number_of_functions_green = number_of_functions_green + 1
            elif function_complexity <= 10:
                function_size_yellow = function_size_yellow + function_size
                number_of_functions_yellow = number_of_functions_yellow + 1
            elif function_complexity <= 25:
                function_size_orange = function_size_orange + function_size
                number_of_functions_orange = number_of_functions_orange + 1
            else:
                function_size_red = function_size_red + function_size
                number_of_functions_red = number_of_functions_red + 1

    return function_size_green, function_size_yellow, function_size_orange, function_size_red, \
        number_of_functions_green, number_of_functions_yellow, number_of_functions_orange, number_of_functions_red


def save_function_complexity_metrics(function_complexity_metrics, report_dir):
    """Save the complexity profile to a csv file."""

    report_file = os.path.join(create_report_directory(report_dir), "function_complexity.csv")
    with open(report_file, 'w') as output:
        csv_writer = csv.writer(output, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL)
        csv_writer.writerow(['Cyclomatic Complexity', 'Lines Of Code', 'Number Of Functions'])
        csv_writer.writerow(["0-5", function_complexity_metrics[0], function_complexity_metrics[4]])
        csv_writer.writerow(["6-10", function_complexity_metrics[1], function_complexity_metrics[5]])
        csv_writer.writerow(["11-25", function_complexity_metrics[2], function_complexity_metrics[6]])
        csv_writer.writerow(["25+", function_complexity_metrics[3], function_complexity_metrics[7]])


def main():
    """The main entry point of the program."""

    args = parse_arguments()
    understand_database = understand.open(args.database)

    function_complexity_metrics = measure_function_complexity(understand_database)
    report_dir = create_report_directory(args.reportdir)
    save_function_complexity_metrics(function_complexity_metrics, report_dir)


if __name__ == "__main__":
    main()
