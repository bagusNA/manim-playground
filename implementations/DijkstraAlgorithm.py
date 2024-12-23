import sys
from typing import Dict, List, Tuple

from tabulate import tabulate

ANSI_COLOR_GREEN = '\033[92m'
ANSI_COLOR_END = '\033[0m'

class Graph:
    def __init__(self):
        self._vertices: List[str] = []
        self._edges: Dict[str, Dict[str, int]] = {}

    @property
    def vertices(self) -> List[str]:
        return self._vertices

    @property
    def edges(self) -> Dict[str, Dict[str, int]]:
        return self._edges

    def add_vertex(self, key: str) -> None:
        """
        Menambahkan vertex ke dalam graph
        :param key:
        :return:
        """
        if key in self._vertices:
            return

        self._vertices.append(key)
        self._edges[key] = {}

        for vertex in self._vertices:
            self._edges[key][vertex] = 0
            self._edges[vertex][key] = 0

    def add_vertices(self, keys: List[str]) -> None:
        """
        Menambahkan list vertex ke dalam graph
        :param keys:
        """
        for key in keys:
            self.add_vertex(key)

    def add_edge(self, vertices: Tuple[str, str], distance: int) -> None:
        """
        Menambahkan edge dari 2 vertex tertentu ke dalam graph
        :param vertices:
        :param distance:
        """
        source_vertex = vertices[0]
        target_vertex = vertices[1]

        if (source_vertex not in self._vertices) or (target_vertex not in self._vertices):
            raise Exception("One or both vertices are not found.")

        self._edges[source_vertex][target_vertex] = distance


class Dijkstra:
    def __init__(self, graph: Graph):
        self._graph: Graph = graph

        self._traveled_vertices: List[str] = []
        self._distance: Dict[str, int] = {}
        self._path: Dict[str, List[str]] = {}

        # Table data
        self._table_result: List[any] = []
        self._printed_traveled_vertices: List[str] = []

    def _find_closest_untraveled_vertex(self) -> str | None:
        """
        Mencari vertex terdekat yang belum dilalui
        :return:
        """
        closest_distance = sys.maxsize
        closest_vertex: str | None = None

        for vertex in self._graph.vertices:
            if self._distance[vertex] < closest_distance and vertex not in self._traveled_vertices:
                closest_distance = self._distance[vertex]
                closest_vertex = vertex

        return closest_vertex

    def _append_table_result(self, vertex: str) -> None:
        self._table_result.append([
            vertex,
            *map(lambda item: self._format_table_result(item[0], item[1], vertex), self._distance.items()),
        ])

    def _format_table_result(self, vertex: str, distance: int, current_vertex: str) -> str:
        if vertex == current_vertex and distance != sys.maxsize:
            self._printed_traveled_vertices.append(vertex)
            return f"{ANSI_COLOR_GREEN}{distance}/{vertex}{ANSI_COLOR_END}"

        if vertex in self._printed_traveled_vertices:
            return " "

        return (
            "∞" if distance == sys.maxsize else f"{distance}/{vertex}"
        )

    def _print_table(self, current_vertex) -> None:
        table = tabulate(
            self._table_result,
            headers=["Traveled", *self._graph.vertices],
            stralign="center",
            numalign="center",
            tablefmt="rounded_grid",
        )

        print(f"\nCurrent vertex: {current_vertex}")
        print(table)

    def _print_result(self, source: str, destination: str):
        print(f"Shortest path from {source} using Dijkstra Algorithm:")

        for vertex, result in self._path.items():
            path = result if vertex == source else [*result, vertex]
            formatted_path = f"{vertex}: {' -> '.join(path)} = {self._distance[vertex]}"

            print(
                formatted_path
                if destination != vertex else
                ANSI_COLOR_GREEN + formatted_path + ANSI_COLOR_END
            )

    def find(self, source: str, destination: str) -> None:
        """
        Isi utama implementasi algoritma dijkstra
        :param source:
        """
        self._path = {vertex: [source] for vertex in self._graph.vertices}
        self._distance = {vertex: sys.maxsize for vertex in self._graph.vertices} # Distance from source
        self._distance[source] = 0

        for _ in self._graph.vertices:
            closest_vertex = self._find_closest_untraveled_vertex()

            self._traveled_vertices.append(closest_vertex)

            for vertex in self._graph.vertices:
                distance_between = self._graph.edges[closest_vertex][vertex]

                if (distance_between > 0) and (vertex not in self._traveled_vertices) and (self._distance[vertex] > self._distance[closest_vertex] + distance_between):
                    self._distance[vertex] = self._distance[closest_vertex] + distance_between

                    if closest_vertex != source:
                        self._path[vertex].append(closest_vertex)

            self._append_table_result(closest_vertex)
            self._print_table(closest_vertex)

        self._print_result(source, destination)

if __name__ == '__main__':
    graph = Graph()

    # Inisialisasi vertex yang digunakan
    graph.add_vertices(["V1", "V2", "V3", "V4", "V5"])

    # Edge dari V1
    graph.add_edge(("V1", "V2"), 7)
    graph.add_edge(("V1", "V3"), 13)

    # Edge dari V2
    graph.add_edge(("V2", "V3"), 4)
    graph.add_edge(("V2", "V4"), 8)

    # Edge dari V3
    graph.add_edge(("V3", "V2"), 5)
    graph.add_edge(("V3", "V4"), 3)
    graph.add_edge(("V3", "V5"), 8)

    # Edge dari V4
    graph.add_edge(("V4", "V2"), 7)
    graph.add_edge(("V4", "V3"), 5)
    graph.add_edge(("V4", "V5"), 2)

    dijkstra = Dijkstra(graph)
    dijkstra.find("V1", "V5")

    # print(dijkstra._graph)
    # print(dijkstra._vertices)
    # print(dijkstra._distance)
    # print(dijkstra._path)
