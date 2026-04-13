from typing import Dict, Tuple, List

Cell = Tuple[int, int]


class Perception:
    """
    Simulates local sensing around the agent.
    """

    def __init__(self, sensing_radius: int = 2):
        self.sensing_radius = sensing_radius

    def sense(self, world, agent_pos: Cell) -> Dict[str, List[Cell]]:
        visible_free = []
        visible_blocked = []

        ar, ac = agent_pos

        for r in range(ar - self.sensing_radius, ar + self.sensing_radius + 1):
            for c in range(ac - self.sensing_radius, ac + self.sensing_radius + 1):
                cell = (r, c)
                if world.in_bounds(cell):
                    if world.is_obstacle(cell):
                        visible_blocked.append(cell)
                    else:
                        visible_free.append(cell)

        return {
            "free": visible_free,
            "blocked": visible_blocked
        }