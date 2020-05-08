import argparse
import os
import re
from anytree import Node, RenderTree, find
from anytree.exporter import DotExporter


def parse_arguments():
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('--excludes', nargs='+')
    parser.add_argument('dir')

    args = parser.parse_args()
    return args


def extract_includes(file_name):
    includes = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            match = re.match(f'#include "(.*.h)"', line)
            if match:
                header_file = os.path.basename(match.group(1))
                includes.append(header_file)
    return includes


def map_includes(directory, excludes):
    include_map = {}
    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if d not in excludes]

        for file in files:
            if file.endswith(('.h', '.hpp', '.c', '.cpp')):
                data = {'includes': extract_includes(os.path.join(root, file)), 'used': False}

                include_map[file] = data

    return include_map


def build_include_graph(node, file_name, include_map, cycles):

    includes = include_map[file_name]['includes']
    include_map[file_name]['used'] = True
    for header_file in includes:
        new_node = Node(header_file, parent=node)
        # if len(include_map[header_file]) != 0 and not include_map[header_file]['used']:
        if header_file in include_map:
            if not include_map[header_file]['used']:
                build_include_graph(new_node, header_file, include_map, cycles)
            else:
                # cycle detected
                cycles.append((new_node, node))


def main():
    args = parse_arguments()
    print(args)

    includes = map_includes(args.dir, args.excludes)

    cycles = []
    root = Node('Waferstage.cpp')
    build_include_graph(root, 'Waferstage.cpp', includes, cycles)

    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

    DotExporter(root).to_picture("root.png")
    # includes = extract_includes(args.dir)
    print(includes)


if __name__ == "__main__":
    main()
