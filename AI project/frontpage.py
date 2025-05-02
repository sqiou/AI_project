import pygame
import sys

def front_page():
    """
    Displays the front page of the game with a background image and a 'Start Game' button.
    """
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Front Page")

    # Colors
    BUTTON_COLOR = (255, 182, 193)  # Light pink
    BUTTON_HOVER_COLOR = (255, 105, 180)  # Hot pink
    TEXT_COLOR = (0, 0, 0)  # Black

    # Load and scale the background image
    try:
        background_image = pygame.image.load("AI project/front.jpeg")  # Replace with your image path
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        pygame.quit()
        sys.exit()

    # Font and button properties
    font = pygame.font.Font(None, 50)
    button_width, button_height = 200, 80
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT - button_height) // 2
    button_text = font.render("Start Game", True, TEXT_COLOR)

    clock = pygame.time.Clock()
    running = True

    while running:
        # Draw the background
        screen.blit(background_image, (0, 0))

        # Get mouse position and clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Check if mouse is over the button
        if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
            color = BUTTON_HOVER_COLOR  # Change color when hovering
            if mouse_click[0]:  # Left mouse button clicked
                print("Start Game button clicked!")
                running = False  # Exit the loop to transition
        else:
            color = BUTTON_COLOR  # Default button color

        # Draw the button
        pygame.draw.rect(screen, color, (button_x, button_y, button_width, button_height), border_radius=10)
        text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_text, text_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit the game
                pygame.quit()
                sys.exit()

        # Update the display
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    front_page()  # Display the front page first
    print("Transitioning to the next part of the game...")
    # Import or call your Level 1 function here
    from Level_1 import level_1
    level_1()  # Start the first level of the game
