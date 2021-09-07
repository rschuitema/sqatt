"""Retrieve all function metrics of the codebase."""

import csv
import os
import understand

from src.reporting.reporting import create_report_directory


def collect_function_metrics(database, output):
    """Collect the function metrics."""

    understand_database = understand.open(database)

    report_file = os.path.join(create_report_directory(output), "function_metrics.csv")
    with open(report_file, "w", encoding="utf-8") as output_file:
        csv_writer = csv.writer(output_file, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)
        csv_writer.writerow(
            [
                "FunctionName",
                "LinesOfCode",
                "CyclomaticComplexity",
                "Fan-in",
                "Fan-out",
                "NumberOfParameters",
            ]
        )

        for func in understand_database.ents("function,method,procedure"):
            metrics = func.metric(
                [
                    "CountLineBlank",
                    "CountLineCode",
                    "CountLineComment",
                    "CountLineInactive",
                    "Cyclomatic",
                    "CountInput",
                    "CountOutput",
                ]
            )

            csv_writer.writerow(
                [
                    func.longname(),
                    metrics["CountLineCode"],
                    metrics["Cyclomatic"],
                    metrics["CountInput"],
                    metrics["CountOutput"],
                    len(func.parameters().split(",")),
                ]
            )
