"""Create a profile for the interface sizes of a codebase."""

import argparse
import csv
import os
import understand


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


def main():
    """The main entry point of the program."""

    args = parse_arguments()
    understand_database = understand.open(args.database)

    green_lines_of_code = 0
    red_lines_of_code = 0
    yellow_lines_of_code = 0
    orange_lines_of_code = 0
    total_lines_of_code = 0

    for func in understand_database.ents("function,method,procedure"):
        number_of_parameters = len(func.parameters().split(","))
        function_metrics = func.metric(["CountLineBlank",
                                        "CountLineCode",
                                        "CountLineComment",
                                        "CountLineInactive",
                                        "Cyclomatic",
                                        "CountInput",
                                        "CountOutput"])

        lines_of_code = function_metrics["CountLineCode"]

        if lines_of_code:
            total_lines_of_code = total_lines_of_code + lines_of_code
            if number_of_parameters <= 2:
                green_lines_of_code = green_lines_of_code + lines_of_code
            elif number_of_parameters <= 4:
                yellow_lines_of_code = yellow_lines_of_code + lines_of_code
            elif number_of_parameters <= 6:
                orange_lines_of_code = orange_lines_of_code + lines_of_code
            elif number_of_parameters >= 7:
                red_lines_of_code = red_lines_of_code + lines_of_code
            else:
                print("Could not determine number of parameters")

    print("green line of code :", green_lines_of_code)
    print("yellow line of code :", yellow_lines_of_code)
    print("orange line of code :", orange_lines_of_code)
    print("red line of code :", red_lines_of_code)
    print("lines of code in functions :", total_lines_of_code)

    report_file = os.path.join(create_report_directory(args.reportdir), "small_interfaces.csv")
    with open(report_file, 'w') as output:
        csvwriter = csv.writer(output, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL)
        csvwriter.writerow(['Number Of Parameters', 'Lines Of Code'])
        csvwriter.writerow(['1-2', green_lines_of_code])
        csvwriter.writerow(['3-4', yellow_lines_of_code])
        csvwriter.writerow(['5-6', orange_lines_of_code])
        csvwriter.writerow(['7+', red_lines_of_code])


if __name__ == "__main__":
    main()
