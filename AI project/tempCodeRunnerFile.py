import pygame
import sys
from frontpage import main as frontpage_main  # Import the main function of frontpage.py
from Level_1 import level_1  # Import the Level 1 logic

def main():
    # Run the front page
    frontpage_main()  # This will handle displaying the front page and the "Start Game" button

    # After exiting the frontpage, start Level 1
    level_1()

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
    sys.exit()