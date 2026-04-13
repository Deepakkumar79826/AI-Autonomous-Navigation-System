import sys
import pygame

from src.config import (
    GRID_ROWS,
    GRID_COLS,
    CELL_SIZE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    WHITE,
    BLACK,
    GRAY,
    LIGHT_BLUE,
    GREEN,
    RED,
    BLUE,
    YELLOW,
    PURPLE,
    ORANGE,
    OBSTACLE_COUNT,
    SENSING_RADIUS,
    DYNAMIC_OBSTACLE_STEP,
    ENABLE_DYNAMIC_OBSTACLE,
    START_POS,
    GOAL_POS,
    SCREENSHOT_DIR,
    METRICS_DIR,
)
from src.simulation.grid_world import GridWorld
from src.perception.perception import Perception
from src.navigation.controller import NavigationController
from src.utils.io_utils import save_metrics


def draw_grid(screen, world, controller):
    screen.fill(WHITE)

    # Draw grid cells
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if world.is_obstacle((r, c)):
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)

            pygame.draw.rect(screen, GRAY, rect, 1)

    # Draw path
    if controller.path:
        for cell in controller.path:
            r, c = cell
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LIGHT_BLUE, rect)

    # Re-draw obstacles above path
    for obstacle in world.get_all_obstacles():
        r, c = obstacle
        rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, BLACK, rect)

    # Start
    sr, sc = world.start
    pygame.draw.rect(screen, GREEN, pygame.Rect(sc * CELL_SIZE, sr * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Goal
    gr, gc = world.goal
    pygame.draw.rect(screen, RED, pygame.Rect(gc * CELL_SIZE, gr * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Agent
    ar, ac = controller.agent_pos
    pygame.draw.rect(screen, BLUE, pygame.Rect(ac * CELL_SIZE, ar * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Sensor range
    sense_rect = pygame.Rect(
        (ac - SENSING_RADIUS) * CELL_SIZE,
        (ar - SENSING_RADIUS) * CELL_SIZE,
        (2 * SENSING_RADIUS + 1) * CELL_SIZE,
        (2 * SENSING_RADIUS + 1) * CELL_SIZE,
    )
    pygame.draw.rect(screen, ORANGE, sense_rect, 2)

    # Bottom info bar
    info_rect = pygame.Rect(0, GRID_ROWS * CELL_SIZE, WINDOW_WIDTH, 80)
    pygame.draw.rect(screen, PURPLE, info_rect)

    font = pygame.font.SysFont("Arial", 20)
    text_1 = font.render(f"Status: {controller.status}", True, WHITE)
    text_2 = font.render(f"Steps: {controller.step_count} | Replans: {controller.replans}", True, YELLOW)
    text_3 = font.render(f"Position: {controller.agent_pos} -> Goal: {controller.goal}", True, WHITE)

    screen.blit(text_1, (10, GRID_ROWS * CELL_SIZE + 8))
    screen.blit(text_2, (10, GRID_ROWS * CELL_SIZE + 32))
    screen.blit(text_3, (10, GRID_ROWS * CELL_SIZE + 54))


def save_screenshot(screen, filename="final_run.png"):
    path = SCREENSHOT_DIR / filename
    pygame.image.save(screen, str(path))
    print(f"[INFO] Screenshot saved to: {path}")


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AI-Based Autonomous Navigation System")
    clock = pygame.time.Clock()

    # Create world
    world = GridWorld(GRID_ROWS, GRID_COLS, START_POS, GOAL_POS)
    world.random_obstacles(OBSTACLE_COUNT)

    # Make sure basic route is possible more often by clearing a few strategic cells
    for cell in [(1, 2), (2, 2), (3, 2), (18, 17), (17, 17), (16, 17)]:
        world.clear_cell(cell)

    perception = Perception(sensing_radius=SENSING_RADIUS)
    controller = NavigationController(world, perception, START_POS, GOAL_POS)

    if not controller.plan_path():
        print("[ERROR] Initial path planning failed.")
        pygame.quit()
        sys.exit()

    running = True
    finished = False

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not finished:
            # Inject one dynamic obstacle to trigger re-planning
            if ENABLE_DYNAMIC_OBSTACLE and controller.step_count == DYNAMIC_OBSTACLE_STEP:
                inserted = world.add_dynamic_obstacle_on_path(controller.path, controller.path_index)
                if inserted:
                    print(f"[INFO] Dynamic obstacle inserted at: {inserted}")

            moved = controller.move_step()

            if controller.agent_pos == controller.goal:
                controller.status = "SUCCESS: GOAL REACHED"
                finished = True
                print("[SUCCESS] Goal reached.")

            elif not moved and controller.agent_pos != controller.goal:
                print("[FAILED] Agent stopped before reaching goal.")
                finished = True

        draw_grid(screen, world, controller)
        pygame.display.flip()

        if finished:
            save_screenshot(screen, "final_run.png")
            metrics_file = save_metrics(controller.get_metrics(), METRICS_DIR)
            print(f"[INFO] Metrics saved to: {metrics_file}")
            pygame.time.delay(2500)
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()