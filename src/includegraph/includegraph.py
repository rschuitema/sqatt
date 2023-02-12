"""Analysis functions for analyzing an include graph for C/C++ code bases."""

import argparse
import os
import re
import shutil
import sys

import networkx as nx
from graphviz import Source


def extract_includes(file_name, include_graph):
    """Extract the include statements from the file and create an edge in the include graph."""

    with open(file_name, "r", encoding="utf-8") as source_file:
        lines = source_file.readlines()
        for line in lines:
            match = re.match(r'#include\s+["<](.*)[">]', line)
            if match:
                target = os.path.basename(match.group(1))
                source = os.path.basename(file_name)
                include_graph.add_edge(source, target)


def build_include_graph(settings):
    """Build an include graph from the provided directory."""

    directory = settings["analysis_directory"]
    excludes = settings["excludes"]

    include_graph = nx.DiGraph()
    for root, dirs, files in os.walk(directory, topdown=True):
        if excludes:
            dirs[:] = [d for d in dirs if d not in excludes]

        for file in files:
            if file.endswith((".h", ".hpp", ".c", ".cpp")):
                extract_includes(os.path.join(root, file), include_graph)

    return include_graph


def show_include_cycles(cycle_list):
    """Show the include cycles on stdout."""

    if len(cycle_list) > 0:
        print("Include cycles found:")
        for cycle in cycle_list:
            print(str(cycle).translate(str.maketrans("", "", "[']")))
    else:
        print("No include cycles found")


def analyze_include_cycles(complete_graph, settings):
    """Analyze the include cycles in the include graph."""

    cycles = nx.simple_cycles(complete_graph)
    cycles = list(cycles)  # make copy of the list created by the generator of simple_cycles
    save_include_cycles(list(cycles), settings)
    show_include_cycles(list(cycles))
    return list(cycles)


def analyze_path(graph, settings):
    """Determine the path between the provided files."""

    source_node = settings["show_path"][0]
    target_node = settings["show_path"][1]
    try:
        path = nx.shortest_path(graph, source=source_node, target=target_node)  # pylint: disable=E1123,E1120

        print(f"The path from {source_node} to {target_node} is:")
        print(str(path).translate(str.maketrans("", "", "[']")))
    except nx.exception.NetworkXNoPath as path_exception:
        print(path_exception)


def setup_report_directory(directory):
    """Create an empty report directory."""

    if os.path.exists(directory):
        shutil.rmtree(directory)

    os.makedirs(directory)

    return directory


def show_include_graph(graph, include_cycles, settings):
    """Show the include graph."""

    report_dir = settings["report_directory"]
    report_file = os.path.join(report_dir, "include_graph")

    pydot_graph = nx.nx_pydot.to_pydot(graph)

    stream = highlight_cycles(str(pydot_graph), include_cycles)
    source = Source(stream, filename=report_file, format="png")
    source.view()


def save_include_cycles(include_cycles, settings):
    """Save the include cycles to a text file."""

    report_file = os.path.join(settings["report_directory"], "include_cycles.txt")
    with open(report_file, "w", encoding="utf-8") as report:
        for cycle in include_cycles:
            cycle_string = str(cycle)
            cycle_string = cycle_string.translate(str.maketrans("", "", "[']"))
            report.write(cycle_string)
            report.write("\n")


def analyze_include_graph_for_file(graph, file_to_analyze):
    """Determine the include graph for the provided file."""

    subgraph = graph.subgraph(nx.shortest_path(graph, file_to_analyze))
    return subgraph


def perform_analysis(analysis):
    """Perform the requested analysis."""

    settings = {
        "analysis_directory": analysis.input,
        "report_directory": analysis.output,
        "analyze_cycles": analysis.cycles,
        "file_to_analyze": analysis.file,
        "excludes": analysis.excludes,
        "show_path": analysis.showpath,
    }

    setup_report_directory(settings["report_directory"])

    graph = build_include_graph(settings)

    if settings["show_path"]:
        analyze_path(graph, settings)

    if settings["file_to_analyze"]:
        graph = analyze_include_graph_for_file(graph, settings["file_to_analyze"])

    cycles = []
    if settings["analyze_cycles"]:
        cycles = analyze_include_cycles(graph, settings)
        cycles = list(cycles)

    show_include_graph(graph, list(cycles), settings)

    return settings


def parse_arguments(args):
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    parser.add_argument("--excludes", nargs="+", help="The directories to exclude from the analysis")
    parser.add_argument("--showpath", nargs=2, help="Show the path from source to target")
    parser.add_argument("--cycles", help="Find all cycles in the includes", action="store_true")
    parser.add_argument("--file", help="The file to build the include graph for")
    parser.add_argument(
        "--output", help="The directory where to place the report.", default=os.path.join(os.getcwd(), "reports")
    )
    parser.add_argument("input", help="The directory to analyze")

    parser.set_defaults(func=perform_analysis)

    return parser.parse_args(args)


def determine_cycle_edges(cycle_nodes):
    """Determine the edges of the nodes in the cycle."""

    edges = []
    for idx, elem in enumerate(cycle_nodes):
        this_element = elem
        next_element = cycle_nodes[(idx + 1) % len(cycle_nodes)]
        edges.append((this_element, next_element))
    return edges


def highlight_cycles(dot_stream, cycle_list):
    """Highlight the include cycles in red."""

    for cycle in cycle_list:
        cycle_edges = determine_cycle_edges(cycle)
        for edge in cycle_edges:
            regex = rf'([<"]{edge[0]}[">] -> [<"]{edge[1]}[">])'
            match = re.search(regex, dot_stream)
            if match:
                replacement = match.group(1) + " [color = red]"
                dot_stream = dot_stream.replace(match.group(1), replacement)

    return dot_stream


def main():
    """Start of the program."""

    args = parse_arguments(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
