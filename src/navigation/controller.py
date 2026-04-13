import time
from typing import Dict, List, Tuple, Optional

from src.planning.astar import astar_search

Cell = Tuple[int, int]


class NavigationController:
    """
    Handles planning, movement, re-planning, and runtime metrics.
    """

    def __init__(self, world, perception, start: Cell, goal: Cell):
        self.world = world
        self.perception = perception
        self.agent_pos = start
        self.goal = goal
        self.path: List[Cell] = []
        self.path_index = 0
        self.step_count = 0
        self.replans = 0
        self.planning_time_total = 0.0
        self.status = "INITIALIZING"

    def plan_path(self) -> bool:
        start_time = time.perf_counter()
        new_path = astar_search(self.world, self.agent_pos, self.goal)
        elapsed = time.perf_counter() - start_time
        self.planning_time_total += elapsed

        if new_path is None:
            self.path = []
            self.status = "FAILED: NO PATH FOUND"
            return False

        self.path = new_path
        self.path_index = 0
        self.status = "PATH PLANNED"
        return True

    def next_waypoint(self) -> Optional[Cell]:
        if not self.path or self.path_index + 1 >= len(self.path):
            return None
        return self.path[self.path_index + 1]

    def move_step(self) -> bool:
        if self.agent_pos == self.goal:
            self.status = "SUCCESS: GOAL REACHED"
            return False

        # Sense environment
        _ = self.perception.sense(self.world, self.agent_pos)

        # Get next target cell
        waypoint = self.next_waypoint()
        if waypoint is None:
            self.status = "RE-PLANNING"
            if not self.plan_path():
                return False
            waypoint = self.next_waypoint()

        if waypoint is None:
            self.status = "FAILED: PATH EMPTY"
            return False

        # If blocked, re-plan
        if self.world.is_obstacle(waypoint):
            self.replans += 1
            self.status = "OBSTACLE DETECTED: RE-PLANNING"
            if not self.plan_path():
                return False
            waypoint = self.next_waypoint()
            if waypoint is None:
                return False

        # Move agent
        self.agent_pos = waypoint
        self.path_index += 1
        self.step_count += 1
        self.status = "MOVING"
        return True

    def get_metrics(self) -> Dict:
        return {
            "final_position": self.agent_pos,
            "goal": self.goal,
            "steps_taken": self.step_count,
            "replans": self.replans,
            "planning_time_total_sec": round(self.planning_time_total, 6),
            "goal_reached": self.agent_pos == self.goal,
            "path_length": len(self.path),
            "status": self.status,
        }