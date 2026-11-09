from .parser import Hub
from collections import deque
import heapq

def move_cost(hub: Hub) -> float:
    if hub.zone == "restricted":
        return 2.0
    if hub.zone == "blocked":
        return float("inf")
    if hub.zone == "priority":
        return 0.9
    return 1.0

def dijkstra(adjacency_list: dict, hubs: dict[str, Hub], start: str, end: str) -> tuple[float, list[str]] | None:
    pq = []
    heapq.heappush(pq, (0, start))
    cheapest = {start: 0}
    parent = {start: None}
  
    while pq:
        cost, current = heapq.heappop(pq)
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return (cost, path[::-1])
        for neighbour in adjacency_list[current]:
            hub = hubs[neighbour]
            m_cost = move_cost(hub)
            if m_cost == float("inf"):
                continue
            new_cost = cost + m_cost
            if new_cost < cheapest.get(neighbour, float("inf")):
                cheapest[neighbour] = new_cost
                parent[neighbour] = current
                heapq.heappush(pq, (new_cost, neighbour))
    return None

def find_paths(
    adjacency_list: dict[str, list[str]],
    hubs: dict[str, Hub],
    start: str,
    end: str)  -> list[list[str]]:
    paths = []
    result = dijkstra(adjacency_list, hubs, start, end)
    if result is None:
        return []
    _, path = result
    paths.append(path)
    for i in range(len(path) - 1):
        a, b = path[i], path[i+1]
        adj_copy = {k: list(v) for k, v in adjacency_list.items()}
        adj_copy[a].remove(b)
        adj_copy[b].remove(a)
        result = dijkstra(adj_copy, hubs, start, end)
        if result is not None:
            _, new_path = result
            if new_path not in paths:
                paths.append(new_path)
    return paths
