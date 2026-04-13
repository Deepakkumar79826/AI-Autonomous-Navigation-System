from pathlib import Path

# Grid configuration
GRID_ROWS = 20
GRID_COLS = 20
CELL_SIZE = 32

# Window configuration
WINDOW_WIDTH = GRID_COLS * CELL_SIZE
WINDOW_HEIGHT = GRID_ROWS * CELL_SIZE + 80
FPS = 8

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 200, 0)
RED = (220, 20, 60)
BLUE = (65, 105, 225)
YELLOW = (255, 215, 0)
PURPLE = (138, 43, 226)
ORANGE = (255, 140, 0)

# Simulation settings
OBSTACLE_COUNT = 60
SENSING_RADIUS = 2
DYNAMIC_OBSTACLE_STEP = 12
ENABLE_DYNAMIC_OBSTACLE = True

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
METRICS_DIR = OUTPUT_DIR / "metrics"
LOGS_DIR = OUTPUT_DIR / "logs"

for folder in [OUTPUT_DIR, SCREENSHOT_DIR, METRICS_DIR, LOGS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Start and goal
START_POS = (1, 1)
GOAL_POS = (18, 18)