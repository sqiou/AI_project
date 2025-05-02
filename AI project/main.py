import pygame
import sys
from Level_1 import level_1  # Import Level 1 game logic
from frontpage import frontpage

def front_page():
    # Screen dimensions
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Front Page")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BUTTON_COLOR = (255, 182, 193)  # Light pink
    BUTTON_HOVER_COLOR = (255, 105, 180)  # Hot pink
    TEXT_COLOR = BLACK

    # Load background image
    try:
        background_image = pygame.image.load("AI_project/front.jpeg")  # Adjust path if necessary
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        pygame.quit()
        sys.exit()

    # Font
    font = pygame.font.Font(None, 50)

    # Button properties
    button_width = 200
    button_height = 80
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT - button_height) // 2

    # Text
    button_text = font.render("Start Game", True, TEXT_COLOR)

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(background_image, (0, 0))  # Draw background

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Check if mouse is over the button
        if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
            color = BUTTON_HOVER_COLOR
            if mouse_click[0]:  # Left mouse button clicked
                running = False  # Exit front page loop to start the game
        else:
            color = BUTTON_COLOR

        # Draw button
        pygame.draw.rect(screen, color, (button_x, button_y, button_width, button_height), border_radius=10)
        text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_text, text_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

def main():
    """
    Main function that runs the front page and transitions to Level 1.
    """
    try:
        # Display the front page
        front_page()

        # After front page, start Level 1
        print("Starting Level 1...")
        level_1()
    except Exception as e:
        print(f"Error occurred: {e}")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()

