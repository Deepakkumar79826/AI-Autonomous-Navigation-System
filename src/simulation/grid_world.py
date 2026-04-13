import random
from typing import List, Tuple, Set

Cell = Tuple[int, int]


class GridWorld:
    """
    Represents the 2D simulation environment.
    0 = free cell
    1 = obstacle
    """

    def __init__(self, rows: int, cols: int, start: Cell, goal: Cell):
        self.rows = rows
        self.cols = cols
        self.start = start
        self.goal = goal
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.dynamic_obstacle_added = False

    def in_bounds(self, cell: Cell) -> bool:
        r, c = cell
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_obstacle(self, cell: Cell) -> bool:
        r, c = cell
        return self.grid[r][c] == 1

    def is_free(self, cell: Cell) -> bool:
        return self.in_bounds(cell) and not self.is_obstacle(cell)

    def set_obstacle(self, cell: Cell) -> None:
        if cell not in [self.start, self.goal] and self.in_bounds(cell):
            r, c = cell
            self.grid[r][c] = 1

    def clear_cell(self, cell: Cell) -> None:
        if self.in_bounds(cell):
            r, c = cell
            self.grid[r][c] = 0

    def random_obstacles(self, count: int, seed: int = 42) -> None:
        random.seed(seed)
        placed = 0
        while placed < count:
            cell = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
            if cell not in [self.start, self.goal] and not self.is_obstacle(cell):
                self.set_obstacle(cell)
                placed += 1

    def get_neighbors(self, cell: Cell) -> List[Cell]:
        r, c = cell
        neighbors = [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
        ]
        valid = [n for n in neighbors if self.is_free(n)]
        return valid

    def get_all_obstacles(self) -> Set[Cell]:
        obstacles = set()
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 1:
                    obstacles.add((r, c))
        return obstacles

    def add_dynamic_obstacle_on_path(self, path: List[Cell], current_step: int) -> Cell | None:
        """
        Adds one obstacle ahead on the current path to force re-planning.
        """
        if self.dynamic_obstacle_added or len(path) < 5:
            return None

        target_index = min(current_step + 2, len(path) - 2)
        cell = path[target_index]

        if cell not in [self.start, self.goal]:
            self.set_obstacle(cell)
            self.dynamic_obstacle_added = True
            return cell

        return None