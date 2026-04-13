import heapq
from typing import Dict, List, Tuple, Optional

Cell = Tuple[int, int]


def heuristic(a: Cell, b: Cell) -> int:
    """
    Manhattan distance heuristic for grid navigation.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from: Dict[Cell, Cell], current: Cell) -> List[Cell]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def astar_search(world, start: Cell, goal: Cell) -> Optional[List[Cell]]:
    """
    Returns the shortest path from start to goal using A*.
    """
    open_heap = []
    heapq.heappush(open_heap, (0, start))

    came_from: Dict[Cell, Cell] = {}
    g_score: Dict[Cell, float] = {start: 0}
    f_score: Dict[Cell, float] = {start: heuristic(start, goal)}

    visited = set()

    while open_heap:
        _, current = heapq.heappop(open_heap)

        if current == goal:
            return reconstruct_path(came_from, current)

        visited.add(current)

        for neighbor in world.get_neighbors(current):
            if neighbor in visited:
                continue

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f_score[neighbor], neighbor))

    return None