import os
import sys

# Project root ko Python path me add karo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.simulation.grid_world import GridWorld
from src.planning.astar import astar_search


def test_astar_finds_path():
    world = GridWorld(rows=5, cols=5, start=(0, 0), goal=(4, 4))
    world.set_obstacle((1, 1))
    world.set_obstacle((1, 2))
    world.set_obstacle((1, 3))

    path = astar_search(world, (0, 0), (4, 4))

    assert path is not None
    assert path[0] == (0, 0)
    assert path[-1] == (4, 4)