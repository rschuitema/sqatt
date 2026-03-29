"""Retrieve all file metrics from an understand database and save them in a csv file."""

import csv
import understand


def sort_metrics(module_metrics, metric):
    """Sort the metrics."""

    sorted_by_value = sorted(module_metrics, key=lambda x: (module_metrics[x][metric] or 0), reverse=True)
    sorted_dict = {}
    for key in sorted_by_value:
        sorted_dict[key] = module_metrics[key]

    return sorted_dict


def save_file_metrics(module, metrics):
    """Save the file metrics to a csv file."""

    with open(module + "_metrics.csv", "w", encoding="utf-8") as output:
        csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)
        csv_writer.writerow(
            [
                "File Name",
                "Cyclomatic Complexity",
                "Number Of Functions",
                "Number Of Classes",
                "Lines",
                "Lines Of Code",
                "Blank Lines",
                "Comment Lines",
                "Inactive Lines",
                "Preprocessor Lines",
            ]
        )

        for filename in metrics:
            file_metrics = metrics[filename]
            csv_writer.writerow(
                [
                    filename,
                    file_metrics["MaxCyclomatic"],
                    file_metrics["CountDeclFunc"] or 0,
                    file_metrics["CountDeclClass"] or 0,
                    file_metrics["CountLine"],
                    file_metrics["CountLineCode"],
                    file_metrics["CountLineBlank"],
                    file_metrics["CountLineComment"],
                    file_metrics["CountLineInactive"],
                    file_metrics["CountLinePreprocessor"],
                ]
            )


def get_module_metrics(module_files):
    """Retrieve all the module metrics."""

    module_metrics = {}
    for file in module_files:
        file_metrics = file.metric(
            [
                "MaxCyclomatic",
                "CountDeclClass",
                "CountDeclFunc",
                "CountLine",
                "CountLineCode",
                "CountLineBlank",
                "CountLineComment",
                "CountLineInactive",
                "CountLinePreprocessor",
            ]
        )

        module_metrics[file.longname()] = file_metrics or 0
    return module_metrics


def find_files_in_module(understand_database, module):
    """Find the files of the module."""

    files = understand_database.lookup(module, "File")

    return files


def collect_file_metrics(database, output, module, sort):
    """Collect the file metrics."""
    print(output)

    understand_database = understand.open(database)
    module_files = find_files_in_module(understand_database, module)
    module_metrics = get_module_metrics(module_files)

    metric = sort
    sorted_module_metrics = sort_metrics(module_metrics, metric)

    for filename in sorted_module_metrics.items():
        print(filename + "," + str(sorted_module_metrics[filename][metric]))

    save_file_metrics(module, sorted_module_metrics)
