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
RED = (255, 0, 0)

# Directions (Up, Right, Down, Left)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Rat and Cat Maze Game")
clock = pygame.time.Clock()

# Image paths (Update these paths to your local paths)
wall_image_path = "images for level 4/rock-texture-wallpaper.jpg"
white_image_path = "images for level 4/8856.jpg"
gate_image_path = "images for level 2/security-gate_11189459.png"
rat_image_path = "images for level 2/mouse.png"
ai_cat_image_path = "images for level 4/AI cat.png"
user_cat_image_path = "images for level 2/cats.png"

# Fixed Maze Layout (1 = Wall, 0 = Path)
maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Helper function to get a random empty cell
def get_random_empty_cell():
    while True:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if maze[x][y] == 0:
            return x, y

# Helper function to draw the maze
def draw_maze():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if maze[row][col] == 0:
                screen.blit(white_image, (col * CELL_SIZE, row * CELL_SIZE))
            else:
                screen.blit(wall_image, (col * CELL_SIZE, row * CELL_SIZE))

# Heuristic function for A* (Manhattan Distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Rat Movement (Improved with memory of last position)
rat_last_position = None  # Keep track of the last position

def markov_rat_move(rat_x, rat_y, goal_x, goal_y):
    global rat_last_position
    possible_moves = []
    
    # Try to find all valid neighboring cells
    for dx, dy in DIRECTIONS:
        next_x, next_y = rat_x + dx, rat_y + dy
        if 0 <= next_x < GRID_SIZE and 0 <= next_y < GRID_SIZE and maze[next_x][next_y] == 0:
            # Avoid the last position
            if (next_x, next_y) != rat_last_position:
                possible_moves.append((next_x, next_y, heuristic((next_x, next_y), (goal_x, goal_y))))
    
    # If there are valid moves, choose the best one
    if possible_moves:
        # Sort by heuristic and choose the best one (nearest to goal)
        possible_moves.sort(key=lambda move: move[2])
        best_moves = [move for move in possible_moves if move[2] == possible_moves[0][2]]
        chosen_move = random.choice(best_moves)
        rat_last_position = (rat_x, rat_y)  # Update last position
        return chosen_move[0], chosen_move[1]
    
    # If no valid moves, make the rat move randomly to avoid it freezing (this should be a fallback)
    print("No valid moves, rat stays in place or moves randomly.")
    return rat_x, rat_y  # Stay in place if no valid moves are found



# AI Cat Movement (Improved path-following logic)
ai_cat_path = []  # Keep track of the current path

def a_star_search(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and maze[neighbor[0]][neighbor[1]] == 0:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []

# AI Cat movement logic
def ai_cat_move():
    global ai_cat_path
    if not ai_cat_path or ai_cat_path[0] != (ai_cat_x, ai_cat_y):  # Recalculate if path is empty or diverges
        ai_cat_path = a_star_search((ai_cat_x, ai_cat_y), (rat_x, rat_y))
    if ai_cat_path:
        return ai_cat_path.pop(0)  # Follow the next step in the path
    return ai_cat_x, ai_cat_y

# Initialize positions
rat_x, rat_y = get_random_empty_cell()
gate_x, gate_y = get_random_empty_cell()
user_cat_x, user_cat_y = get_random_empty_cell()
ai_cat_x, ai_cat_y = get_random_empty_cell()

# Load images
wall_image = pygame.image.load(wall_image_path)
white_image = pygame.image.load(white_image_path)
gate_image = pygame.image.load(gate_image_path)
rat_image = pygame.image.load(rat_image_path)
ai_cat_image = pygame.image.load(ai_cat_image_path)
user_cat_image = pygame.image.load(user_cat_image_path)

# Resize images to fit within CELL_SIZE
wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))
white_image = pygame.transform.scale(white_image, (CELL_SIZE, CELL_SIZE))
gate_image = pygame.transform.scale(gate_image, (CELL_SIZE, CELL_SIZE))
rat_image = pygame.transform.scale(rat_image, (CELL_SIZE, CELL_SIZE))
ai_cat_image = pygame.transform.scale(ai_cat_image, (CELL_SIZE, CELL_SIZE))
user_cat_image = pygame.transform.scale(user_cat_image, (CELL_SIZE, CELL_SIZE))


# Main game loop
running = True
while running:
    screen.fill(BLACK)
    draw_maze()
    screen.blit(rat_image, (rat_y * CELL_SIZE, rat_x * CELL_SIZE))
    screen.blit(gate_image, (gate_y * CELL_SIZE, gate_x * CELL_SIZE))
    screen.blit(user_cat_image, (user_cat_y * CELL_SIZE, user_cat_x * CELL_SIZE))
    screen.blit(ai_cat_image, (ai_cat_y * CELL_SIZE, ai_cat_x * CELL_SIZE))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Move UP
    if keys[pygame.K_UP]:
        if user_cat_x > 0 and maze[user_cat_x - 1][user_cat_y] == 0:
            user_cat_x -= 1
            print(f"Moved UP to ({user_cat_x}, {user_cat_y})")

    # Move DOWN
    if keys[pygame.K_DOWN]:
        if user_cat_x < GRID_SIZE - 1 and maze[user_cat_x + 1][user_cat_y] == 0:
            user_cat_x += 1
            print(f"Moved DOWN to ({user_cat_x}, {user_cat_y})")

    # Move LEFT
    if keys[pygame.K_LEFT]:
        if user_cat_y > 0 and maze[user_cat_x][user_cat_y - 1] == 0:
            user_cat_y -= 1
            print(f"Moved LEFT to ({user_cat_x}, {user_cat_y})")

    # Move RIGHT
    if keys[pygame.K_RIGHT]:
        if user_cat_y < GRID_SIZE - 1 and maze[user_cat_x][user_cat_y + 1] == 0:
            user_cat_y += 1
            print(f"Moved RIGHT to ({user_cat_x}, {user_cat_y})")

    # Rat movement
    rat_x, rat_y = markov_rat_move(rat_x, rat_y, gate_x, gate_y)

    # Check for collision after rat moves
    if (rat_x, rat_y) == (user_cat_x, user_cat_y):
        print("User cat caught the rat!")
        running = False

    # AI Cat movement
    ai_cat_x, ai_cat_y = ai_cat_move()

    # Check for collision with AI cat
    if (rat_x, rat_y) == (ai_cat_x, ai_cat_y):
        print("AI cat caught the rat!")
        running = False

    # Check for rat reaching the gate
    if (rat_x, rat_y) == (gate_x, gate_y):
        print("Rat escaped!")
        running = False

    # Update display and tick
    pygame.display.flip()
    clock.tick(4)

pygame.quit()
sys.exit()

