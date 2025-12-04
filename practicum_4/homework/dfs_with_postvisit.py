from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from practicum_4.dfs import GraphTraversal
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DfsViaLifoQueueWithPostvisit(GraphTraversal):
    def run(self, node: Any) -> None:
        stack = deque([(node, 0)])
        visited = set()

        while stack:
            curr, state = stack.pop()

            if state == 0:
                if curr not in visited:
                    visited.add(curr)
                    self.previsit(curr)

                    stack.append((curr, 1))
                    reversed_neighbors = reversed(list(self.G.neighbors(curr)))
                    for u in reversed_neighbors:
                        if u not in visited:
                            stack.append((u, 0))
            else:
                self.postvisit(curr)

class DfsViaLifoQueueWithPrinting(DfsViaLifoQueueWithPostvisit):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit node {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit node {node}")


if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist(
        r"C:\Users\Alena\PycharmProjects\spbu-fundamentals-of-algorithms\practicum_4\simple_graph_10_nodes.edgelist",
        create_using=nx.Graph
    )
    # plot_graph(G)

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")

