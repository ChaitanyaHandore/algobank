import heapq
from typing import Dict, Tuple, List

class GraphRouter:
    """
    Interbank routing system using Dijkstra's algorithm.
    Demonstrates priority queues, adjacency lists, and shortest-path optimization.
    """

    def __init__(self):
        self.cgraph: Dict[str, List[Tuple[str, float]]] = {}

    def add_edge(self, u: str, v: str, w: float):
        """Add a bidirectional edge with transaction cost w."""
        self.cgraph.setdefault(u, []).append((v, w))
        self.cgraph.setdefault(v, []).append((u, w))

    def shortest_path(self, start: str, end: str) -> Tuple[float, List[str]]:
        """
        Compute the least-cost route between two banks.
        Returns (total_cost, path). If unreachable, returns (inf, []).
        """
        if start not in self.cgraph or end not in self.cgraph:
            return float("inf"), []

        pq = [(0, start, [])]  # (cost, node, path)
        visited = set()

        while pq:
            cost, node, path = heapq.heappop(pq)
            if node in visited:
                continue
            visited.add(node)
            path = path + [node]

            if node == end:
                return cost, path

            for neigh, wt in self.cgraph.get(node, []):
                if neigh not in visited:
                    heapq.heappush(pq, (cost + wt, neigh, path))

        return float("inf"), []