import pygame
# import sys
# import heapq
# import random

# # Constants
# GRID_SIZE = 20
# CELL_SIZE = 30
# SCREEN_SIZE = GRID_SIZE * CELL_SIZE
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# ORANGE = (255, 165, 0)

# # Directions
# DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# # Initialize Pygame
# pygame.init()
# screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
# pygame.display.set_caption("Rat and Cat Maze Game")
# clock = pygame.time.Clock()

# # Fixed Maze Layout (1 = Wall, 0 = Path)
# maze = [ 
#     [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
#     [1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
#     [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
#     [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
#     [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#     [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
#     [0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
#     [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
#     [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#     [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
#     [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0],
#     [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
#     [0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#     [0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0]
# ]

# # Positions
# start_pos = (0, 0)
# gate_pos = (GRID_SIZE - 1, GRID_SIZE - 1)
# cat_pos = (GRID_SIZE // 2, GRID_SIZE // 2)

# # Heuristic function for A*
# def heuristic(a, b):
#     return abs(a[0] - b[0]) + abs(a[1] - b[1])

# # Generate food particles
# food_particles = set()
# while len(food_particles) < 10:  # Generate 10 food particles
#     x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
#     if maze[y][x] == 0 and (x, y) not in [start_pos, gate_pos, cat_pos]:
#         food_particles.add((x, y))

# # Load images
# rat_image = pygame.image.load("mouse.png")
# cat_image = pygame.image.load("cat.png")

# # Scale images to fit the grid cells
# rat_image = pygame.transform.scale(rat_image, (CELL_SIZE, CELL_SIZE))
# cat_image = pygame.transform.scale(cat_image, (CELL_SIZE, CELL_SIZE))

# # Draw the grid with images
# def draw_grid():
#     for y in range(GRID_SIZE):
#         for x in range(GRID_SIZE):
#             rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
#             color = WHITE
#             if maze[y][x] == 1:
#                 color = BLACK
#                 pygame.draw.rect(screen, color, rect)
#             elif (x, y) == gate_pos:
#                 color = BLUE
#                 pygame.draw.rect(screen, color, rect)
#             elif (x, y) in food_particles:
#                 color = ORANGE
#                 pygame.draw.rect(screen, color, rect)

#             # Draw the rat
#             if (x, y) == rat_pos:
#                 screen.blit(rat_image, rect.topleft)
#             # Draw the cat
#             elif (x, y) == cat_pos:
#                 screen.blit(cat_image, rect.topleft)
#             else:
#                 pygame.draw.rect(screen, color, rect)
#             pygame.draw.rect(screen, BLACK, rect, 1)

# # A* algorithm with escape priority and cat avoidance
# def a_star_escape(start, goal, cat_pos):
#     open_set = []
#     heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, []))
#     closed_set = set()

#     while open_set:
#         _, cost, current, path = heapq.heappop(open_set)

#         if current in closed_set:
#             continue
#         path = path + [current]
#         closed_set.add(current)

#         if current == goal:
#             return path

#         for dx, dy in DIRECTIONS:
#             neighbor = (current[0] + dx, current[1] + dy)

#             if (
#                 0 <= neighbor[0] < GRID_SIZE
#                 and 0 <= neighbor[1] < GRID_SIZE
#                 and maze[neighbor[1]][neighbor[0]] == 0
#                 and neighbor not in closed_set
#             ):
#                 distance_to_cat = heuristic(neighbor, cat_pos)
#                 food_bonus = 10 if neighbor in food_particles else 0
#                 cat_penalty = -20 if distance_to_cat <= 2 else 0

#                 escape_bonus = 50 if neighbor == goal else 0
#                 total_cost = cost + 1 - food_bonus - cat_penalty - escape_bonus
#                 heapq.heappush(
#                     open_set,
#                     (total_cost + heuristic(neighbor, goal), cost + 1, neighbor, path),
#                 )

#     return None

# # Main Game Loop
# rat_pos = start_pos
# rat_life = 0  # Rat's life (score)
# rat_moves = 0  # Counter for slowing down the rat
# cat_catch_count = 0  # Count how many times the cat caught the rat
# running = True

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Move the cat
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_UP]:
#         cat_pos = (cat_pos[0], max(0, cat_pos[1] - 1))
#     elif keys[pygame.K_DOWN]:
#         cat_pos = (cat_pos[0], min(GRID_SIZE - 1, cat_pos[1] + 1))
#     elif keys[pygame.K_LEFT]:
#         cat_pos = (max(0, cat_pos[0] - 1), cat_pos[1])
#     elif keys[pygame.K_RIGHT]:
#         cat_pos = (min(GRID_SIZE - 1, cat_pos[0] + 1), cat_pos[1])

#     # Calculate the rat's path with escape priority
#     if rat_moves % 2 == 0:  # Rat moves only on every second frame
#         rat_path = a_star_escape(rat_pos, gate_pos, cat_pos) or []

#         # Move the rat along the path
#         if rat_path:
#             rat_pos = rat_path[1]  # Move to the next step

#     rat_moves += 1

#     # Check for food collection
#     if rat_pos in food_particles:
#         food_particles.remove(rat_pos)
#         rat_life += 1
#         print(f"Rat collected food! Life: {rat_life}")

#     # Check for game conditions
#     if rat_pos == gate_pos:
#         print("The rat has escaped!")
#         running = False
#     elif rat_pos == cat_pos:
#         cat_catch_count += 1
#         if cat_catch_count >= 2:
#             print("The cat caught the rat twice! Game over.")
#             running = False
#         else:
#             print("The cat caught the rat! Run, rat, run!")

#     # Render the game
#     screen.fill(WHITE)
#     draw_grid()
#     pygame.display.flip()
#     clock.tick(10)

# pygame.quit()
# sys.exit()