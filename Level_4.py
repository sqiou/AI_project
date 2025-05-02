import pygame
import sys
import heapq
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Constants
GRID_SIZE = 20
CELL_SIZE = 37
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Directions (Up, Right, Down, Left)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def level_4():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Rat and Cat Maze Game")
    clock = pygame.time.Clock()

     #music
    pygame.mixer.init()
    pygame.mixer.music.load("games music.mp3")  # Replace with your music file
    pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
    pygame.mixer.music.play(-1) 

    # Image paths
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

    # Rat Movement
    rat_last_position = None

    def markov_rat_move(rat_x, rat_y, goal_x, goal_y):
        nonlocal rat_last_position
        possible_moves = []
        for dx, dy in DIRECTIONS:
            next_x, next_y = rat_x + dx, rat_y + dy
            if 0 <= next_x < GRID_SIZE and 0 <= next_y < GRID_SIZE and maze[next_x][next_y] == 0:
                if (next_x, next_y) != rat_last_position:
                    possible_moves.append((next_x, next_y, heuristic((next_x, next_y), (goal_x, goal_y))))
        if possible_moves:
            possible_moves.sort(key=lambda move: move[2])
            best_moves = [move for move in possible_moves if move[2] == possible_moves[0][2]]
            chosen_move = random.choice(best_moves)
            rat_last_position = (rat_x, rat_y)
            return chosen_move[0], chosen_move[1]
        print("No valid moves, rat stays in place or moves randomly.")
        return rat_x, rat_y

    # AI Cat Movement
    ai_cat_path = []

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

    def ai_cat_move():
        nonlocal ai_cat_path
        if not ai_cat_path or ai_cat_path[0] != (ai_cat_x, ai_cat_y):
            ai_cat_path = a_star_search((ai_cat_x, ai_cat_y), (rat_x, rat_y))
        if ai_cat_path:
            return ai_cat_path.pop(0)
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

    # Resize images
    wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))
    white_image = pygame.transform.scale(white_image, (CELL_SIZE, CELL_SIZE))
    gate_image = pygame.transform.scale(gate_image, (CELL_SIZE, CELL_SIZE))
    rat_image = pygame.transform.scale(rat_image, (CELL_SIZE, CELL_SIZE))
    ai_cat_image = pygame.transform.scale(ai_cat_image, (CELL_SIZE, CELL_SIZE))
    user_cat_image = pygame.transform.scale(user_cat_image, (CELL_SIZE, CELL_SIZE))

    # Main game loop
    running = True
    result = None
    while running:
        screen.fill(BLACK)
        draw_maze()
        screen.blit(rat_image, (rat_y * CELL_SIZE, rat_x * CELL_SIZE))
        screen.blit(gate_image, (gate_y * CELL_SIZE, gate_x * CELL_SIZE))
        screen.blit(user_cat_image, (user_cat_y * CELL_SIZE, user_cat_x * CELL_SIZE))
        screen.blit(ai_cat_image, (ai_cat_y * CELL_SIZE, ai_cat_x * CELL_SIZE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and user_cat_x > 0 and maze[user_cat_x - 1][user_cat_y] == 0:
            user_cat_x -= 1
            print(f"Moved UP to ({user_cat_x}, {user_cat_y})")
        if keys[pygame.K_DOWN] and user_cat_x < GRID_SIZE - 1 and maze[user_cat_x + 1][user_cat_y] == 0:
            user_cat_x += 1
            print(f"Moved DOWN to ({user_cat_x}, {user_cat_y})")
        if keys[pygame.K_LEFT] and user_cat_y > 0 and maze[user_cat_x][user_cat_y - 1] == 0:
            user_cat_y -= 1
            print(f"Moved LEFT to ({user_cat_x}, {user_cat_y})")
        if keys[pygame.K_RIGHT] and user_cat_y < GRID_SIZE - 1 and maze[user_cat_x][user_cat_y + 1] == 0:
            user_cat_y += 1
            print(f"Moved RIGHT to ({user_cat_x}, {user_cat_y})")

        rat_x, rat_y = markov_rat_move(rat_x, rat_y, gate_x, gate_y)
        if (rat_x, rat_y) == (user_cat_x, user_cat_y):
            result = "User cat caught the rat!"
            running = False
        ai_cat_x, ai_cat_y = ai_cat_move()
        if (rat_x, rat_y) == (ai_cat_x, ai_cat_y):
            result = "AI cat caught the rat!"
            running = False
        if (rat_x, rat_y) == (gate_x, gate_y):
            result = "Rat escaped!"
            running = False

        pygame.display.flip()
        clock.tick(4)
    pygame.mixer.music.stop()
    pygame.quit()
    if result:
        show_scoreboard(result)



def show_scoreboard(result):
    def replay():
        messagebox.showinfo("Action", "Replay the current level!")
        root.destroy()
        level_4()  # Assuming level_1 is the function for replaying the current level
    def next_level():
        messagebox.showinfo("Action", "Proceeding to the next level!")
        root.destroy()
    def exit_game():
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            root.destroy()
            pygame.quit()
            sys.exit()  # To exit the game

    root = tk.Tk()
    root.title("Game Progression")
    root.geometry("800x800")

    bg_image = Image.open("pic2.webp")  # Replace with your scoreboard image
    bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    result_label = tk.Label(root, text=result, font=("Helvetica", 24), bg="gray", fg="white")
    result_label.pack(pady=20)

    button_frame = tk.Frame(root, bg="gray", bd=5)
    button_frame.place(relx=0.5, rely=0.8, anchor="center")

    replay_button = tk.Button(button_frame, text="Replay", font=("Helvetica", 14), bg="blue", fg="white", command=replay)
    replay_button.grid(row=0, column=0, padx=10)

    next_button = tk.Button(button_frame, text="Next Level", font=("Helvetica", 14), bg="green", fg="white", command=next_level)
    next_button.grid(row=0, column=1, padx=10)

    exit_button = tk.Button(button_frame, text="Exit", font=("Helvetica", 14), bg="red", fg="white", command=exit_game)
    exit_button.grid(row=0, column=2, padx=10)

    root.mainloop()
level_4()