import pygame
import sys
import heapq
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Level 1 Function
def level_1():
    GRID_SIZE = 20
    CELL_SIZE = 37
    SCREEN_SIZE = GRID_SIZE * CELL_SIZE
    BLACK = (0, 0, 0)

    # Directions
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Rat Maze Game - Level 1")
    clock = pygame.time.Clock()
    #music
    pygame.mixer.init()
    pygame.mixer.music.load("games music.mp3")  # Replace with your music file
    pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
    pygame.mixer.music.play(-1) 

    # Load images
    rat_image = pygame.image.load("imageslvl1/mouse.png")
    rat_image = pygame.transform.scale(rat_image, (CELL_SIZE, CELL_SIZE))

    cat_image = pygame.image.load("imageslvl1/cat.png")
    cat_image = pygame.transform.scale(cat_image, (CELL_SIZE, CELL_SIZE))

    barricade_image = pygame.image.load("imageslvl1/barricade.png")
    barricade_image = pygame.transform.scale(barricade_image, (CELL_SIZE, CELL_SIZE))

    start_image = pygame.image.load("imageslvl1/startgate1.png")
    start_image = pygame.transform.scale(start_image, (CELL_SIZE, CELL_SIZE))

    exit_image = pygame.image.load("imageslvl1/endgate1.png")
    exit_image = pygame.transform.scale(exit_image, (CELL_SIZE, CELL_SIZE))

    # Fixed Maze Layout
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

    # A* Algorithm
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
        screen.fill(BLACK)
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if maze[y][x] == 1:
                    screen.blit(barricade_image, rect.topleft)
                else:
                    pygame.draw.rect(screen, BLACK, rect)

        screen.blit(start_image, (start_pos[0] * CELL_SIZE, start_pos[1] * CELL_SIZE))
        screen.blit(exit_image, (gate_pos[0] * CELL_SIZE, gate_pos[1] * CELL_SIZE))

    # Main Game Loop
    rat_pos = start_pos
    rat_move_counter = 0
    rat_move_delay = 6
    running = True
    result = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and cat_pos[1] > 0:
                    cat_pos = (cat_pos[0], cat_pos[1] - 1)
                elif event.key == pygame.K_DOWN and cat_pos[1] < GRID_SIZE - 1:
                    cat_pos = (cat_pos[0], cat_pos[1] + 1)
                elif event.key == pygame.K_LEFT and cat_pos[0] > 0:
                    cat_pos = (cat_pos[0] - 1, cat_pos[1])
                elif event.key == pygame.K_RIGHT and cat_pos[0] < GRID_SIZE - 1:
                    cat_pos = (cat_pos[0] + 1, cat_pos[1])

        rat_path = a_star(rat_pos, gate_pos, avoid=cat_pos) or []
        rat_move_counter += 1
        if rat_path and len(rat_path) > 1 and rat_move_counter >= rat_move_delay:
            rat_pos = rat_path[1]
            rat_move_counter = 0

        if rat_pos == gate_pos:
            result = "The rat has escaped!"
            running = False
        elif rat_pos == cat_pos:
            result = "The cat caught the rat!"
            running = False

        draw_grid()
        screen.blit(rat_image, (rat_pos[0] * CELL_SIZE, rat_pos[1] * CELL_SIZE))
        screen.blit(cat_image, (cat_pos[0] * CELL_SIZE, cat_pos[1] * CELL_SIZE))
        pygame.display.flip()
        clock.tick(20)
    pygame.mixer.music.stop()
    pygame.quit()
    if result:
        show_scoreboard(result)

# Scoreboard Function
def show_scoreboard(result):
    def replay():
        messagebox.showinfo("Action", "Replay the current level!")
        root.destroy()
        level_1()
   
    def next_level():
        messagebox.showinfo("Action", "Proceeding to the next level!")
        root.destroy()
        level_2()

    def exit_game():
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            root.destroy()

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
level_1()
from Level_2 import level_2