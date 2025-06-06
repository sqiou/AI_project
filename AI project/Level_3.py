import pygame
import sys
import heapq
import random

# Constants
GRID_SIZE = 20
CELL_SIZE = 37  
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BEIGE = (245, 245, 220)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)  # Color for hearts

# Directions
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Rat and Cat Maze Game")
clock = pygame.time.Clock()

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
    [0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0]
]

# Positions
start_pos = (0, 0)
gate_pos = (GRID_SIZE - 1, GRID_SIZE - 1)
cat_pos = (GRID_SIZE // 2, GRID_SIZE // 2)

# Heuristic function for A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Generate food particles
food_particles = set()
while len(food_particles) < 10:  # Generate 10 food particles
    x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
    if maze[y][x] == 0 and (x, y) not in [start_pos, gate_pos, cat_pos]:
        food_particles.add((x, y))

# Load images
rat_image = pygame.image.load("AI project/imageslvl3/rat1.png")
cat_image = pygame.image.load("AI project/imageslvl3/cat1.png")
start_image = pygame.image.load("AI project/imageslvl3/startgate1.png")
end_image = pygame.image.load("AI project/imageslvl3/endgate1.png")
wall_image = pygame.image.load("AI project/imageslvl3/wall-image.png")  # Image for walls
food_image = pygame.image.load("AI project/imageslvl3/cheese.png")  # Load the image for food
heart_image = pygame.image.load("AI project/imageslvl3/heart.png")  # Image for hearts (lives)

# Scale images to fit the grid cells
rat_image = pygame.transform.scale(rat_image, (CELL_SIZE, CELL_SIZE))
cat_image = pygame.transform.scale(cat_image, (CELL_SIZE, CELL_SIZE))
start_image = pygame.transform.scale(start_image, (CELL_SIZE, CELL_SIZE))
end_image = pygame.transform.scale(end_image, (CELL_SIZE, CELL_SIZE))
wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))
food_image = pygame.transform.scale(food_image, (CELL_SIZE, CELL_SIZE))  # Scale food image
heart_image = pygame.transform.scale(heart_image, (CELL_SIZE // 2, CELL_SIZE // 2))  # Scale heart image

# Draw the grid with images
def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            # Draw the walls using the wall image
            if maze[y][x] == 1:
                screen.blit(wall_image, rect.topleft)
            # Draw the start and end positions
            elif (x, y) == gate_pos:
                screen.blit(end_image, rect.topleft)  # End position image
            elif (x, y) == start_pos:
                screen.blit(start_image, rect.topleft)  # Start position image
            # Draw the food particles using the food image
            elif (x, y) in food_particles:
                screen.blit(food_image, rect.topleft)  # Draw food image
            # Draw the rat
            if (x, y) == rat_pos:
                screen.blit(rat_image, rect.topleft)
            # Draw the cat
            elif (x, y) == cat_pos:
                screen.blit(cat_image, rect.topleft)
            # Draw a border for each cell
            pygame.draw.rect(screen, BLACK, rect, 1)

# Function to randomize the rat's position
def randomize_rat_position():
    while True:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if maze[y][x] == 0 and (x, y) != gate_pos and (x, y) != cat_pos:
            return (x, y)

# Draw rat's hearts (lives)
def draw_lives():
    for i in range(rat_life):
        screen.blit(heart_image, (i * CELL_SIZE + 5, 5))

# A* algorithm with escape priority and cat avoidance
def a_star_escape(start, goal, cat_pos):
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
            ):
                distance_to_cat = heuristic(neighbor, cat_pos)
                food_bonus = 10 if neighbor in food_particles else 0
                cat_penalty = -20 if distance_to_cat <= 2 else 0

                escape_bonus = 50 if neighbor == goal else 0
                total_cost = cost + 1 - food_bonus - cat_penalty - escape_bonus
                heapq.heappush(
                    open_set,
                    (total_cost + heuristic(neighbor, goal), cost + 1, neighbor, path),
                )

    return None

# Main Game Loop
rat_pos = start_pos
rat_life = 1  # Rat's initial lives (hearts)
rat_moves = 0  # Counter for slowing down the rat
cat_catch_count = 0  # Count how many times the cat caught the rat
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the cat
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        cat_pos = (cat_pos[0], max(0, cat_pos[1] - 1))
    elif keys[pygame.K_DOWN]:
        cat_pos = (cat_pos[0], min(GRID_SIZE - 1, cat_pos[1] + 1))
    elif keys[pygame.K_LEFT]:
        cat_pos = (max(0, cat_pos[0] - 1), cat_pos[1])
    elif keys[pygame.K_RIGHT]:
        cat_pos = (min(GRID_SIZE - 1, cat_pos[0] + 1), cat_pos[1])

    # Calculate the rat's path with escape priority
    if rat_moves % 2 == 0:  # Rat moves only on every second frame
        if rat_life > 0:  # Only move if the rat has lives
            rat_path = a_star_escape(rat_pos, gate_pos, cat_pos) or []
            if rat_path:
                rat_pos = rat_path[1]  # Move to the next step

    rat_moves += 1

    # Check for food collection
    if rat_pos in food_particles:
        food_particles.remove(rat_pos)
        rat_life += 1
        print(f"Rat collected food!")

    # Check for game conditions
    if rat_pos == gate_pos:
        print("The rat has escaped!")
        running = False
    elif rat_pos == cat_pos:
        cat_catch_count += 1
        if rat_life > 1:  # Decrease life only if there are remaining lives
            rat_life -= 1  # Decrease the rat's life (heart) when the cat catches it
            print(f"The cat caught the rat! Remaining lives: {rat_life}")
            # Randomize the rat's position after being caught
            rat_pos = randomize_rat_position()
        else:
            # If rat_life reaches 0, game over
            print("The cat caught the rat too many times! Game over.")
            running = False

    # Render the game
    screen.fill(WHITE)
    draw_grid()
    draw_lives()  # Draw rat's hearts representing lives
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
