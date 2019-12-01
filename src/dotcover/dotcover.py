"""Parse the coverage results of the tool dotcover."""

import argparse
import csv
import os

import xmltodict


def parse_arguments():
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="dotcover result file to parse")
    parser.add_argument("--reportdir", help="directory where to place the report")
    parser.add_argument("--namespace", help="the namespace for which the coverage needs to be calculated")
    parser.add_argument("--verbose", help="print details on console", action="store_true")
    args = parser.parse_args()
    return args


def read_coverage(filename):
    """Read the coverage into a dictionary."""

    with open(filename) as input_file:
        doc = xmltodict.parse(input_file.read())

    return doc


def create_report_directory(directory):
    """Create the report directory."""

    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def get_coverage_of_namespace(assembly, covered_lines, name_space, total_lines):
    """Get the coverage of a namespace."""

    assembly_name = assembly['@Name']
    assembly_covered_lines = assembly['@CoveredStatements']
    assembly_total_lines = assembly['@TotalStatements']
    if assembly_name.startswith(name_space):
        total_lines = total_lines + int(assembly_total_lines)
        covered_lines = covered_lines + int(assembly_covered_lines)
    return covered_lines, total_lines


def determine_coverage_of_namespace(xml_doc, name_space):
    """Determine the coverage of a namespace."""

    assemblies = (xml_doc['Root']['Assembly'])
    total_lines = 0
    covered_lines = 0

    if not isinstance(assemblies, list):
        covered_lines, total_lines = get_coverage_of_namespace(assemblies, covered_lines, name_space, total_lines)
    else:
        for assembly in assemblies:
            covered_lines, total_lines = get_coverage_of_namespace(assembly, covered_lines, name_space, total_lines)

    coverage = 100 * (covered_lines/total_lines)
    return coverage


def determine_namespaces(xml_doc):
    """Determine all the namespaces that dotcover analyzed."""

    namespaces = set()
    assemblies = (xml_doc['Root']['Assembly'])

    if not isinstance(assemblies, list):
        name = get_namespaces(assemblies['@Name'], '.')
        namespaces.update(name)
        return namespaces

    for assembly in assemblies:
        assembly_name = assembly['@Name']
        name = get_namespaces(assembly_name, '.')
        namespaces.update(name)

    return namespaces


def get_namespaces(line, separator):
    """Get all the namespaces defined in line based upon the provided separator."""

    namespaces = set()
    if len(line) > 0 and line not in namespaces:
        namespaces.add(line)

        parts = line.rsplit(separator, 1)
        while parts[0] not in namespaces:
            namespaces.add(parts[0])
            parts = parts[0].rsplit(separator, 1)

    return namespaces


def determine_coverage_per_namespace(xml_doc):
    """Determine the coverage per namespace."""

    namespace_coverage = {}
    namespaces = determine_namespaces(xml_doc)

    for namespace in namespaces:
        namespace_coverage[namespace] = determine_coverage_of_namespace(xml_doc, namespace)

    return namespace_coverage


def save_coverage_per_namespace(coverage_per_namespace, report_dir):
    """Save the coverage per namespace."""

    report_file = os.path.join(report_dir, "coverage_per_namespace.csv")

    with open(report_file, 'w') as output:
        csv_writer = csv.writer(output, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL)
        csv_writer.writerow(['Namespace', 'Coverage'])
        for item in coverage_per_namespace:
            csv_writer.writerow([item, coverage_per_namespace[item]])


def main():
    """Start of the program."""

    args = parse_arguments()

    xml_doc = read_coverage(args.filename)

    if args.namespace:
        coverage = determine_coverage_of_namespace(xml_doc, args.namespace)
        print(coverage)

    coverage_per_namespace = determine_coverage_per_namespace(xml_doc)
    report_dir = create_report_directory(args.reportdir)
    save_coverage_per_namespace(coverage_per_namespace, report_dir)

    if args.verbose:
        for name in coverage_per_namespace:
            print(name, " : ", coverage_per_namespace[name])


if __name__ == "__main__":
    main()
