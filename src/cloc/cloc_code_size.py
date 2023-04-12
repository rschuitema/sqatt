"""Analyze the code size using the tool cloc."""
# import csv
# import os
#
# from src.cloc.cloc_measure import measure_lines_of_code, get_size_metrics
# from src.profile.colors import PROFILE_COLORS
# from src.profile.show import make_donut
# from src.reporting.reporting import create_report_directory
#
#
# def show_code_profile(profile, title):
#     """Show the profile in a donut."""
#
#     labels = ["Blank Lines", "Lines of Code", "Comment Lines"]
#     values = [profile["SUM"]["blank"], profile["SUM"]["code"], profile["SUM"]["comment"]]
#
#     fig = make_donut(labels, values, f"{title} code <br> breakdown", PROFILE_COLORS)
#     fig.show()
#
#
# def write_code_size_metrics(csv_writer, metrics):
#     """Write the code size metrics to the csv file."""
#
#     language_metrics = metrics["SUM"]
#     csv_writer.writerow(
#         [
#             language_metrics["blank"],
#             language_metrics["code"],
#             language_metrics["comment"],
#         ]
#     )
#
#
# def write_code_size_header(csv_writer):
#     """Write the header to the csv file."""
#
#     csv_writer.writerow(
#         [
#             "Blank Lines",
#             "Lines Of Code",
#             "Comment Lines",
#         ]
#     )
#
#
# def calculate_comment_to_code_ratio(production_code_metrics, test_code_metrics):
#     """Calculate the ratio between the comments and the lines of code."""
#
#     lines_of_code = production_code_metrics["SUM"]["code"] + test_code_metrics["SUM"]["code"]
#     comment_lines = production_code_metrics["SUM"]["comment"] + test_code_metrics["SUM"]["comment"]
#
#     return float(comment_lines) / float(lines_of_code)
#
#
# def calculate_test_code_to_production_code_ratio(production_code_metrics, test_code_metrics):
#     """Calculate the ratio between the test code and the production code."""
#
#     lines_of_code = production_code_metrics["SUM"]["code"]
#     lines_of_test_code = test_code_metrics["SUM"]["code"]
#
#     return float(lines_of_test_code) / float(lines_of_code)
#
#
# def save_code_metrics(production_code_size_file, production_code_metrics):
#     """Save the code metrics to a file."""
#
#     with open(production_code_size_file, "w", encoding="utf-8") as output:
#         csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)
#
#         write_code_size_header(csv_writer)
#         write_code_size_metrics(csv_writer, production_code_metrics)
#
#
# def save_ratios(comment_code_ratio, test_code_ratio):
#     """Save the metric ratios to a file."""
#
#     print(comment_code_ratio, test_code_ratio)
#
#
# def save_code_type_profile(report_dir, metrics):
#     """Save the code metrics to a file."""
#
#     report_file = os.path.join(report_dir, "code_type_profile.csv")
#     with open(report_file, "w", encoding="utf-8") as output:
#         csv_writer = csv.writer(output, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)
#
#         write_code_type_header(csv_writer)
#         write_code_type_metrics(csv_writer, metrics)
#
#
# def write_code_type_metrics(csv_writer, metrics):
#     """Save the code type metrics."""
#
#     if metrics:
#         csv_writer.writerow(
#             [
#                 metrics["production"]["SUM"]["code"],
#                 metrics["test"]["SUM"]["code"],
#                 metrics["generated"]["SUM"]["code"],
#                 metrics["third_party"]["SUM"]["code"],
#             ]
#         )
#
#
# def write_code_type_header(csv_writer):
#     """Save the code type metrics header."""
#
#     csv_writer.writerow(
#         [
#             "Production",
#             "Test",
#             "Generated",
#             "Third Party",
#         ]
#     )
#
#
# def analyze_size_per_code_type(settings):
#     """Analyze the code size for all code types."""
#
#     metrics = {}
#     report_dir = create_report_directory(settings["report_directory"])
#
#     for code_type in settings["code_type"]:
#         report_file = os.path.join(report_dir, f"{code_type}_code_volume_profile.csv")
#         analysis_filter = settings[f"{code_type}_filter"]
#         measure_lines_of_code(settings["analysis_directory"], report_file, analysis_filter)
#         metrics[code_type] = get_size_metrics(report_file)
#         save_code_metrics(report_file, metrics[code_type])
#
#     save_code_type_profile(report_dir, metrics)
#     return metrics
#
#
# def show_code_type_profile(metrics):
#     """Show the profile in a donut."""
#
#     labels = ["Production", "Test", "Third Party", "Generated"]
#     values = [
#         metrics["production"]["SUM"]["code"],
#         metrics["test"]["SUM"]["code"],
#         metrics["third_party"]["SUM"]["code"],
#         metrics["generated"]["SUM"]["code"],
#     ]
#
#     fig = make_donut(labels, values, "Code type breakdown", PROFILE_COLORS)
#     fig.show()
#
#
# def analyze_code_size(settings):
#     """Analyze the code size."""
#
#     metrics = analyze_size_per_code_type(settings)
#
#     comment_code_ratio = calculate_comment_to_code_ratio(metrics["production"], metrics["test"])
#     test_code_ratio = calculate_test_code_to_production_code_ratio(metrics["production"], metrics["test"])
#
#     save_ratios(comment_code_ratio, test_code_ratio)
#
#     show_code_profile(metrics["production"], "Production")
#     show_code_type_profile(metrics)
