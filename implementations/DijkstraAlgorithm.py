import sys
from typing import Dict, List, Tuple


class Dijkstra:
    def __init__(self):
        self._vertices: List[str] = []
        self._graph: Dict[str, Dict[str, int]] = {}
        self._traveled_vertices: List[str] = []
        self._distance: Dict[str, int] = {}
        self._path: Dict[str, List[str]] = {}

    def add_vertex(self, key: str) -> None:
        """
        Menambahkan vertex ke dalam graph
        :param key:
        :return:
        """
        if key in self._vertices:
            return

        self._vertices.append(key)
        self._graph[key] = {}

        for vertex in self._vertices:
            self._graph[key][vertex] = 0
            self._graph[vertex][key] = 0

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

        self._graph[source_vertex][target_vertex] = distance

    def _find_closest_untraveled_vertex(self) -> str | None:
        """
        Mencari vertex terdekat yang belum dilalui
        :return:
        """
        closest_distance = sys.maxsize
        closest_vertex: str | None = None

        for vertex in self._vertices:
            if self._distance[vertex] < closest_distance and vertex not in self._traveled_vertices:
                closest_distance = self._distance[vertex]
                closest_vertex = vertex

        return closest_vertex

    def run(self, source: str) -> None:
        """
        Isi utama implementasi algoritma dijkstra
        :param source:
        """
        self._path = {vertex: [source] for vertex in self._vertices}
        self._distance = {vertex: sys.maxsize for vertex in self._vertices}
        self._distance[source] = 0

        for _ in self._vertices:
            closest_vertex = self._find_closest_untraveled_vertex()

            self._traveled_vertices.append(closest_vertex)

            for vertex in self._vertices:
                distance_between = self._graph[closest_vertex][vertex]

                if (distance_between > 0) and (vertex not in self._traveled_vertices) and (self._distance[vertex] > self._distance[closest_vertex] + distance_between):
                    self._distance[vertex] = self._distance[closest_vertex] + distance_between

                    if closest_vertex != source:
                        self._path[vertex].append(closest_vertex)


if __name__ == '__main__':
    dijkstra = Dijkstra()

    # Inisialisasi vertex yang digunakan
    dijkstra.add_vertices(["V1", "V2", "V3", "V4", "V5"])

    # Edge dari V1
    dijkstra.add_edge(("V1", "V2"), 7)
    dijkstra.add_edge(("V1", "V3"), 13)

    # Edge dari V2
    dijkstra.add_edge(("V2", "V3"), 4)
    dijkstra.add_edge(("V2", "V4"), 8)

    # Edge dari V3
    dijkstra.add_edge(("V3", "V2"), 5)
    dijkstra.add_edge(("V3", "V4"), 3)
    dijkstra.add_edge(("V3", "V5"), 8)

    # Edge dari V4
    dijkstra.add_edge(("V4", "V2"), 7)
    dijkstra.add_edge(("V4", "V3"), 5)
    dijkstra.add_edge(("V4", "V5"), 2)

    dijkstra.run("V1")

    # print(dijkstra._graph)
    # print(dijkstra._vertices)
    print(dijkstra._distance)
    print(dijkstra._path)
