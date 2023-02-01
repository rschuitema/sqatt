"""Measure the lines of code."""
import csv
import os
import re

from src.facility.subprocess import Subprocess


def measure_lines_of_code(input_dir, report_file, measure_filter):
    """Measure the lines of code using a filter."""

    if "--match-d" in measure_filter:
        # this path is a workaround for the error in cloc with the --match-d option
        measure_lines_of_code_as_txt(input_dir, report_file, measure_filter)
    else:
        cloc_measure_as_csv(input_dir, report_file, measure_filter)


def get_sub_directories(directory_name):
    """Get all subdirectories of a directory."""

    sub_folders = [f.path for f in os.scandir(directory_name) if f.is_dir()]
    for dir_name in list(sub_folders):
        sub_folders.extend(get_sub_directories(dir_name))

    return sub_folders


def convert_measurement_results_to_csv(combined_results_file, report_file):
    """Convert the combined measurements results file into a csv file."""

    with open(combined_results_file + ".lang", "r", newline="\n", encoding="utf-8") as txt_file:
        lines = txt_file.readlines()
        lines.pop(0)
        my_lines = [line for line in lines if not line.startswith("----")]
        my_lines = [line for line in my_lines if not line.startswith("Language")]

        with open(report_file, 'w', encoding="utf-8") as out_file:
            csv_writer = csv.writer(out_file, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)
            csv_writer.writerow(["language", "files", "blank", "comment", "code"])
            for line in my_lines:
                line = line.replace("SUM:", "SUM")
                values = line.split()
                csv_writer.writerow(values)


def measure_lines_of_code_as_txt(input_dir, report_file, measure_filter):
    """Measure the lines of code and store the results in a txt file."""

    report_dir = os.path.dirname(report_file)

    sub_folders = get_folders_matching_filter(input_dir, measure_filter)
    measure_lines_of_code_per_folder(report_file, sub_folders)

    combined_results_file = combine_measurement_results(report_dir)
    convert_measurement_results_to_csv(combined_results_file, report_file)


def combine_measurement_results(report_dir):
    """
    Combine the measurement results of all the individual measurements.
    It will combine all the .txt files in the 'report_dir'.
    """

    text_files = [os.path.join(report_dir, d) for d in os.listdir(report_dir) if d.endswith('.txt')]
    combined_results_file = os.path.join(report_dir, "combined")
    cloc_combine_results(combined_results_file, text_files)

    return combined_results_file


def measure_lines_of_code_per_folder(report_file, sub_folders):
    """Measure the lines of code for each folder in 'sub_folders' and store the results as txt."""

    i = 0
    for folder in sub_folders:
        cloc_measure_as_txt(folder, f"{os.path.splitext(report_file)[0]}_{i}.txt")
        i = i + 1


def get_folders_matching_filter(input_dir, measure_filter):
    """
    Get the sub-folders of 'input_dir' that match the criteria of the 'measure_filer'.
    The filter is specified in the format of --match-d of cloc.
    """

    filter_regex = measure_filter.split('=')[1]
    filter_regex = re.sub(r'(\w+)', lambda m: m.group(1) + '\\b', filter_regex)  # (.*(test\b|tst\b).*)
    filter_regex = f'(.*{filter_regex}.*)'

    sub_folders = get_sub_directories(input_dir)
    sub_folders[:] = [d for d in sub_folders if re.search(filter_regex, d)]

    return sub_folders


def cloc_measure_as_txt(input_folder, report_file):
    """Measure the lines of code with cloc and store the result in a txt file."""

    measure_language_size_command = [
        "cloc",
        "--hide-rate",
        "--out",
        report_file,
        input_folder,
    ]
    process = Subprocess(measure_language_size_command, verbose=1)
    process.execute()


def cloc_combine_results(report_file, text_files):
    """Combine result with cloc."""

    combine_command = [
        "cloc",
        "--sum-reports",
        "--out",
        report_file,
    ]
    combine_command.extend(text_files)
    process = Subprocess(combine_command, verbose=1)
    process.execute()


def cloc_measure_as_csv(input_dir, report_file, measure_filter):
    """Measure the lines of code with cloc and store the result in a txt file."""

    measure_language_size_command = [
        "cloc",
        "--csv",
        "--csv-delimiter=,",
        "--hide-rate",
        f"--report-file={report_file}",
        measure_filter,
        input_dir,
    ]

    process = Subprocess(measure_language_size_command, verbose=1)
    process.execute()


def get_size_metrics(report_file, reader=None):
    """Get the size metrics from file."""

    metrics = {}

    with open(report_file, "r", newline="\n", encoding="utf-8") as csv_file:
        csv_reader = reader or csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            language_metric = {
                "files": row["files"],
                "blank": row["blank"],
                "comment": row["comment"],
                "code": row["code"],
            }
            metrics[row["language"]] = language_metric

    return metrics
