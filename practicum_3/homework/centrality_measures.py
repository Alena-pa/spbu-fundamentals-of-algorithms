from typing import Any, Protocol
from itertools import combinations

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph


class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...


def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    if len(G) <= 1:
        return {v: 0 for v in G}

    result = {}
    for v in G:
        dist = nx.single_source_shortest_path_length(G, v)
        dist_sum = len(dist) - 1
        if dist_sum == 0:
            result[v] = 0
        else:
            total_dist = sum(dist.values())
            result[v] = dist_sum / total_dist
    return result


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    result = {v: 0 for v in G}
    nodes = list(G)
    for s, t in combinations(nodes, 2):
        try:
            all_path = list(nx.all_shortest_paths(G, s, t))
        except nx.NetworkXError:
            continue
        number_of_paths = len(all_path)
        for path in all_path:
            for v in path[1: -1]:
                result[v] += 1 / number_of_paths
    if len(nodes) > 2:
        scale = 1 / ((len(nodes) - 1) * (len(nodes) - 2) / 2)
        result = {key: value * scale for key, value in result.items()}
    return result


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    if len(G) == 0: return {}
    result = {v: 1 for v in G}

    for i in range(1000):
        new_result = {}
        for v in G:
            total = sum(result[u] for u in G.neighbors(v))
            new_result[v] = total
        norm = float(np.linalg.norm(list(new_result.values())))
        for v in new_result:
            new_result[v] /= norm
        diff = max(abs(new_result[v] - result[v]) for v in G)
        if diff < 1e-6:
            break
        result = new_result
    return result


def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")


if __name__ == "__main__":
    G = nx.karate_club_graph()

    plot_centrality_measure(G, closeness_centrality)
    plot_centrality_measure(G, betweenness_centrality)
    plot_centrality_measure(G, eigenvector_centrality)

