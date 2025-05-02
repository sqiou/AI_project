import pygame
import sys
import heapq
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

# Constants
GRID_SIZE = 20
CELL_SIZE = 37
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Directions
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Example Level 2 Function Placeholder
def level_2():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Rat Maze Game - Level 2")
    clock = pygame.time.Clock()

     #music
    pygame.mixer.init()
    pygame.mixer.music.load("games music.mp3")  # Replace with your music file
    pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
    pygame.mixer.music.play(-1) 

    # Fixed Maze Layout (1 = Wall, 0 = Path)
    maze = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    # Positions
    start_pos = (0, 0)
    gate_pos = (GRID_SIZE - 1, GRID_SIZE - 1)
    cat_pos = (GRID_SIZE // 2, GRID_SIZE // 2)

    # Add three rats
    rat_positions = [(0, 0), (0, 8), (1, 7)]  # Three rats starting at different positions

    # Load images
    start_image = pygame.image.load("images for level 2/Start.png")  # Start block image
    start_image = pygame.transform.scale(start_image, (CELL_SIZE, CELL_SIZE))

    wall_image = pygame.image.load("images for level 2/jail_7991341.png")  # Wall block image (PDF converted to PNG)
    wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))

    gate_image = pygame.image.load("images for level 2/security-gate_11189459.png")  # Goal/gate image
    gate_image = pygame.transform.scale(gate_image, (CELL_SIZE, CELL_SIZE))

    cat_image = pygame.image.load("images for level 2/cats.png")  # Cat image
    cat_image = pygame.transform.scale(cat_image, (CELL_SIZE, CELL_SIZE))

    rat_image = pygame.image.load("images for level 2/mouse.png")  # Rat image
    rat_image = pygame.transform.scale(rat_image, (CELL_SIZE, CELL_SIZE))

    # Load the white block image
    white_block_image = pygame.image.load("images for level 2/color.png")
    white_block_image = pygame.transform.scale(white_block_image, (CELL_SIZE, CELL_SIZE))

    def draw_grid():
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                # Draw the wall block image
                if maze[y][x] == 1:
                    screen.blit(wall_image, rect.topleft)

                # Draw the white block image for empty paths
                elif maze[y][x] == 0:
                    screen.blit(white_block_image, rect.topleft)

                # Draw the start block image
                if (x, y) == start_pos:
                    screen.blit(start_image, rect.topleft)

                # Draw the gate image
                if (x, y) == gate_pos:
                    screen.blit(gate_image, rect.topleft)

                # Draw the rats
                for rat_pos in rat_positions:
                    if (x, y) == rat_pos:
                        screen.blit(rat_image, rect.topleft)

                # Draw grid border
                pygame.draw.rect(screen, BLACK, rect, 1)

        # Draw the cat last to ensure it appears on top of other elements
        cat_rect = pygame.Rect(cat_pos[0] * CELL_SIZE, cat_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        screen.blit(cat_image, cat_rect.topleft)

    def a_star(start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: manhattan_distance(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return reconstruct_path(came_from, current)

            for dx, dy in DIRECTIONS:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and maze[neighbor[1]][neighbor[0]] == 0:
                    tentative_g_score = g_score[current] + 1
                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def greedy_avoidance(rat, cat):
        max_distance = -1
        best_move = None
        for dx, dy in DIRECTIONS:
            neighbor = (rat[0] + dx, rat[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and maze[neighbor[1]][neighbor[0]] == 0:
                distance = manhattan_distance(neighbor, cat)
                if distance > max_distance:
                    max_distance = distance
                    best_move = neighbor
        return best_move if best_move else rat

    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def reconstruct_path(came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]
    

    rat_paths = {i: [] for i in range(len(rat_positions))}  # Track paths by index for each rat
    running = True
    AVOIDANCE_THRESHOLD = 5

    while running:
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
              running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
           cat_pos = (cat_pos[0], max(0, cat_pos[1] - 1))
        elif keys[pygame.K_DOWN]:
           cat_pos = (cat_pos[0], min(GRID_SIZE - 1, cat_pos[1] + 1))
        elif keys[pygame.K_LEFT]:
           cat_pos = (max(0, cat_pos[0] - 1), cat_pos[1])
        elif keys[pygame.K_RIGHT]:
           cat_pos = (min(GRID_SIZE - 1, cat_pos[0] + 1), cat_pos[1])

    # Update each rat independently
        for i, rat_pos in enumerate(rat_positions):
        # If rat is near the cat, use greedy avoidance strategy
           if manhattan_distance(rat_pos, cat_pos) <= AVOIDANCE_THRESHOLD:
               next_move = greedy_avoidance(rat_pos, cat_pos)
               rat_paths[i] = [next_move]  # Update the rat's path to only avoid cat
           elif rat_pos != gate_pos:  # Only re-calculate path if the rat hasn't reached the goal
               if not rat_paths[i] or rat_pos == rat_paths[i][-1]:
                   rat_paths[i] = a_star(rat_pos, gate_pos) or []

           if rat_paths[i]:
               rat_positions[i] = rat_paths[i].pop(0)  # Move the rat along its path

    # Check for game termination
        rats_escaped = all(rat == gate_pos for rat in rat_positions)
        any_rat_caught = any(rat == cat_pos for rat in rat_positions)

        if rats_escaped or any_rat_caught:
           running = False
           if rats_escaped:
               result = "The rat has escaped!"
           if any_rat_caught:
               result = "The cat caught the rat!"
    
        screen.fill(WHITE)
        draw_grid()
        pygame.display.flip()
        clock.tick(5)

    pygame.mixer.music.stop()
    pygame.quit()
    if result:
        show_scoreboard(result)
    # Scoreboard Function

def show_scoreboard(result):
    def replay():
        messagebox.showinfo("Action", "Replay the current level!")
        root.destroy()
        level_2()  # Assuming level_1 is the function for replaying the current level
    def next_level():
        messagebox.showinfo("Action", "Proceeding to the next level!")
        root.destroy()
        level_3()
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


# Start the game
level_2()
from Level_3 import level_3
