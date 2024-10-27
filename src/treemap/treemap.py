import os
from pathlib import Path

import networkx
import pandas
import plotly.graph_objects as go
import plotly.express as px


def determine_parents_and_labels(analysis_directory):
    labels = []
    parents = []
    values = []

    for root, dirs, files in os.walk(analysis_directory):
        labels.append(str(Path(root)))
        parents.append(str(Path(root).parent))
        values.append(sum(os.path.getsize(os.path.join(root, file)) for file in files))

        for file in files:
            labels.append(str(Path(root, file)))
            parents.append(str(Path(root)))
            values.append(os.path.getsize(os.path.join(root, file)))

    data_frame = pandas.DataFrame(
        {
            "labels": pandas.Series(labels),
            "parents": pandas.Series(parents),
            "values": pandas.Series(values),
        }

    )
    return data_frame


def show_treemap(data_frame):
    fig = px.treemap(
        names=data_frame["labels"],
        values=data_frame["values"],
        parents=data_frame["parents"],
        color=data_frame["values"],
        color_continuous_scale='RdYlGn'
    )
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


def main():
    """Start of the program."""

    analysis_directory = 'D:\\Projects\\github\\sqatt-for-testing\\src'
    data_frame = determine_parents_and_labels(analysis_directory)
    show_treemap(data_frame)
    pandas.DataFrame.to_csv(data_frame, "tree.csv")
    print(data_frame)


def make_graph():
    graph = networkx.Graph()
    level = 0
    for root, dirs, files in os.walk('D:\\Projects\\github\\sqatt-for-testing\\src'):
        print("--------------------------")
        print(f"root:{root}")
        print(f"dirs:{dirs}")
        print(f"files:{files}")
        for directory in dirs:
            graph.add_edge(os.path.basename(root), directory)
            graph.nodes[directory]["level"] = level + 1
            graph.nodes[directory]["abspath"] = os.path.abspath(directory)
        for file in files:
            graph.add_edge(os.path.basename(root), file)
            graph.nodes[file]["level"] = level + 1
            graph.nodes[file]["abspath"] = os.path.abspath(file)

        graph.nodes[os.path.basename(root)]["level"] = level
        graph.nodes[os.path.basename(root)]["abspath"] = os.path.abspath(root)
        level = level + 1
    print(graph)
    # print(networkx.has_path(graph, 'src', 'cloc_analysis.py'))
    # print(graph.nodes["cloc_analysis.py"]["abspath"])
    # print(graph.nodes["src"]["level"])
    # node_list = list(graph.nodes)
    # print(node_list)
    data_frame = networkx.to_pandas_adjacency(graph)
    pandas.DataFrame.to_csv(data_frame, "tree.csv")
    print(data_frame)


if __name__ == "__main__":
    main()
