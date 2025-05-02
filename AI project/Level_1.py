import pygame
import sys
import heapq

def level_1():
    pass
    GRID_SIZE = 20
    # Constants
    CELL_SIZE = 37
    SCREEN_SIZE = GRID_SIZE * CELL_SIZE
    BLACK = (0, 0, 0)

    # Directions
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Rat Maze Game")
    clock = pygame.time.Clock()

    # Load images
    rat_image = pygame.image.load("AI project/imageslvl1/mouse.png")  # Replace with your rat image path
    rat_image = pygame.transform.scale(rat_image, (CELL_SIZE, CELL_SIZE))

    cat_image = pygame.image.load("AI project/imageslvl1/cat.png")  # Replace with your cat image path
    cat_image = pygame.transform.scale(cat_image, (CELL_SIZE, CELL_SIZE))

    barricade_image = pygame.image.load("AI project/imageslvl1/barricade.png")  # Replace with barricade image path
    barricade_image = pygame.transform.scale(barricade_image, (CELL_SIZE, CELL_SIZE))

    start_image = pygame.image.load("AI project/imageslvl1/startgate1.png")  # Replace with start image path
    start_image = pygame.transform.scale(start_image, (CELL_SIZE, CELL_SIZE))

    exit_image = pygame.image.load("AI project/imageslvl1/endgate1.png")  # Replace with exit image path
    exit_image = pygame.transform.scale(exit_image, (CELL_SIZE, CELL_SIZE))

    # Fixed Maze Layout (1 = Wall, 0 = Path)
    maze = [
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0],
    ]

    # Positions
    start_pos = (0, 0)
    gate_pos = (GRID_SIZE - 1, GRID_SIZE - 1)
    cat_pos = (GRID_SIZE // 2, GRID_SIZE // 2)

    # Heuristic function for A*
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # A* algorithm
    def a_star(start, goal, avoid=None):
        open_set = []
        heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, []))
        closed_set = set()

        while open_set:
            _, cost, current, path = heapq.heappop(open_set)

            if current in closed_set:
                continue
            path = path + [current]
            closed_set.add(current)

            if current == goal:
                return path

            for dx, dy in DIRECTIONS:
                neighbor = (current[0] + dx, current[1] + dy)

                if (
                    0 <= neighbor[0] < GRID_SIZE
                    and 0 <= neighbor[1] < GRID_SIZE
                    and maze[neighbor[1]][neighbor[0]] == 0
                    and neighbor not in closed_set
                    and (not avoid or heuristic(neighbor, avoid) > 1)
                ):
                    heapq.heappush(open_set, (cost + 1 + heuristic(neighbor, goal), cost + 1, neighbor, path))

        return None

    # Draw the grid
    def draw_grid():
        screen.fill(BLACK)  # Clear the screen
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                if maze[y][x] == 1:
                    screen.blit(barricade_image, rect.topleft)  # Draw barricade image on walls
                else:
                    pygame.draw.rect(screen, BLACK, rect)  # Draw plain black background for paths

        # Draw start and exit images
        screen.blit(start_image, (start_pos[0] * CELL_SIZE, start_pos[1] * CELL_SIZE))
        screen.blit(exit_image, (gate_pos[0] * CELL_SIZE, gate_pos[1] * CELL_SIZE))

    # Main Game Loop
    rat_pos = start_pos
    rat_move_counter = 0  # Counter to slow down rat's speed
    rat_move_delay = 6  # Reduced delay for faster rat movement
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Cat movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and cat_pos[1] > 0:
                    cat_pos = (cat_pos[0], cat_pos[1] - 1)
                elif event.key == pygame.K_DOWN and cat_pos[1] < GRID_SIZE - 1:
                    cat_pos = (cat_pos[0], cat_pos[1] + 1)
                elif event.key == pygame.K_LEFT and cat_pos[0] > 0:
                    cat_pos = (cat_pos[0] - 1, cat_pos[1])
                elif event.key == pygame.K_RIGHT and cat_pos[0] < GRID_SIZE - 1:
                    cat_pos = (cat_pos[0] + 1, cat_pos[1])

        # Calculate the rat's path using A*
        rat_path = a_star(rat_pos, gate_pos, avoid=cat_pos) or []

        # Move the rat along the path (slow it down using a counter)
        rat_move_counter += 1
        if rat_path and len(rat_path) > 1 and rat_move_counter >= rat_move_delay:
            rat_pos = rat_path[1]  # Move to the next step
            rat_move_counter = 0  # Reset the counter

        # Check for game conditions
        if rat_pos == gate_pos:
            print("The rat has escaped!")
            running = False
        elif rat_pos == cat_pos:
            print("The cat caught the rat!")
            running = False

        # Render the game
        draw_grid()
        screen.blit(rat_image, (rat_pos[0] * CELL_SIZE, rat_pos[1] * CELL_SIZE))  # Draw the rat
        screen.blit(cat_image, (cat_pos[0] * CELL_SIZE, cat_pos[1] * CELL_SIZE))  # Draw the cat
        pygame.display.flip()
        clock.tick(30)  # Increased frame rate for smoother animations

    pygame.quit()
    sys.exit()

#start game
level_1()

