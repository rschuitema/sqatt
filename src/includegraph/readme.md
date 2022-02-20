# Includegraph

cdThis python tool can analyze the include dependencies for C/C++ code. It has the following features:

* List the include cycles
* Show the include graph
* Show the include path from one file to another file

This first implementation has the following limitations:

* It can report a cycle that is not actually a cycle when two files have exactly the same name
* It does not follow the include path algorithm of the compiler

## Prerequisites

To perform its tasks it makes use of the libraries: [networkx](https://networkx.org/)
and [graphviz](https://pypi.org/project/graphviz/). Install these dependencies with:

```text
pip install networkx
pip install graphviz
```

## Usage

### Show the include graph of the code in a directory

```text
python includegraph.py <directory_to_analyze>
```

This will output the graph in a reports directory.

### Show the include graph for a specific file

```text
python includegraph.y --file <filename> <directory_to_analyze>
```

This will output the graph for the specified file in a reports directory.

### Determine the include cycles

```text
python includegraph.py --cycles <directory_to_analyze>
```

This will output the include cycles that have been found on the console. Each line contains a cycle. The last file in
the line includes the first file of this line.

Example console output: File1 File2 File3

This means that File1 includes File2 and File2 includes File3 and File3 includes File1

### Specifying the output directory

```text
python includegraph.py --output <output_directory> <directory_to_analyze>
```

With the --output option the results wil be placed in the specified directory.

### Excluding directories from analysis

```text
python includegraph.py --excludes dir1 dir2 <directory_to_analyze>
```

With the --excludes option certain directories can be excluded from being analyzed. Multiple directories can be excluded
be separating them with a space.
