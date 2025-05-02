import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # To handle background image scaling

def replay():
    messagebox.showinfo("Action", "Replay the current level!")

def next_level():
    messagebox.showinfo("Action", "Proceeding to the next level!")

def exit_game():
    if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
        root.destroy()

# Initialize the main window
root = tk.Tk()
root.title("Game Progression")
root.geometry("600x600")  # Set the window size

# Load and set the background image
bg_image = Image.open("pic2.webp")  # Replace 'scoreboard.webp' with your image path
bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)  # Updated constant
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Cover the entire window

# Add buttons
button_frame = tk.Frame(root, bg="gray", bd=5)
button_frame.place(relx=0.5, rely=0.8, anchor="center")  # Positioned near the bottom

replay_button = tk.Button(
    button_frame, text="Replay", font=("Helvetica", 14), bg="blue", fg="white", command=replay
)
replay_button.grid(row=0, column=0, padx=10)

next_button = tk.Button(
    button_frame, text="Next Level", font=("Helvetica", 14), bg="green", fg="white", command=next_level
)
next_button.grid(row=0, column=1, padx=10)

exit_button = tk.Button(
    button_frame, text="Exit Game", font=("Helvetica", 14), bg="red", fg="white", command=exit_game
)
exit_button.grid(row=0, column=2, padx=10)

# Run the main loop
root.mainloop()