"""Retrieve all file metrics from an understand database and save them in a csv file."""

import argparse
import csv
import understand


def parse_arguments():
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("database",
                        help="understand database to parse")
    parser.add_argument("-m",
                        "--module",
                        help="module to analyze")
    parser.add_argument("-s",
                        "--sort",
                        help="sort on the specified metric",
                        choices=["MaxCyclomatic",
                                 "CountLine",
                                 "CountLineCode",
                                 "CountLineBlank",
                                 "CountLineComment",
                                 "CountLineInactive",
                                 "CountLinePreprocessor",
                                 "CountDeclFile",
                                 "CountDeclFunction",
                                 "CountDeclClass"])
    args = parser.parse_args()
    return args


def sort_metrics(module_metrics, metric):
    """Sort the metrics."""

    sorted_by_value = sorted(module_metrics, key=lambda x: (module_metrics[x][metric] or 0), reverse=True)
    sorted_dict = {}
    for key in sorted_by_value:
        sorted_dict[key] = module_metrics[key]

    return sorted_dict


def save_file_metrics(module, metrics):
    """Save the file metrics to a csv file."""

    with open(module + '_metrics.csv', 'w') as output:
        csv_writer = csv.writer(output, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL)
        csv_writer.writerow(['File Name',
                             'Cyclomatic Complexity',
                             'Lines',
                             'Lines Of Code',
                             'Blank Lines',
                             'Comment Lines',
                             'Inactive Lines',
                             'Preprocessor Lines',
                             'Number Of Files',
                             'Number Of Functions',
                             'Number Of Classes'])

        for filename in metrics:
            file_metrics = metrics[filename]
            csv_writer.writerow([filename,
                                 file_metrics["MaxCyclomatic"],
                                 file_metrics["CountLine"],
                                 file_metrics["CountLineCode"],
                                 file_metrics["CountLineBlank"],
                                 file_metrics["CountLineComment"],
                                 file_metrics["CountLineInactive"],
                                 file_metrics["CountLinePreprocessor"],
                                 file_metrics["CountDeclFile"] or 0,
                                 file_metrics["CountDeclFunc"] or 0,
                                 file_metrics["CountDeclClass"]or 0])


def get_module_metrics(module_files):
    """Retrieve all the module metrics."""

    module_metrics = {}
    for file in module_files:
        file_metrics = file.metric(["MaxCyclomatic",
                                    "CountLine",
                                    "CountLineCode",
                                    "CountLineBlank",
                                    "CountLineComment",
                                    "CountLineInactive",
                                    "CountLinePreprocessor",
                                    "CountDeclFile",
                                    "CountDeclFunc",
                                    "CountDeclClass"])

        module_metrics[file.longname()] = file_metrics or 0
    return module_metrics


def find_files_in_module(understand_database, module):
    """Find the files of the module."""

    files = understand_database.lookup(module, "File")

    return files


def main():
    """Main entry of the program."""

    args = parse_arguments()
    understand_database = understand.open(args.database)
    module = args.module

    module_files = find_files_in_module(understand_database, module)
    module_metrics = get_module_metrics(module_files)

    metric = args.sort
    sorted_module_metrics = sort_metrics(module_metrics, metric)

    for filename in sorted_module_metrics:
        print(filename + "," + str(sorted_module_metrics[filename][metric]))

    save_file_metrics(module, sorted_module_metrics)


if __name__ == "__main__":
    main()
