import tkinter as tk
import math

class InfinitePathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Infinite Loop Eye Tracking Game")
        self.root.geometry("800x600")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")  # Background is white
        self.canvas.pack()

        # Initialize variables
        self.ball = None
        self.ball_size = 30
        self.speed = 0.02  # Speed of the ball
        self.t = 0  # Parameter for the parametric equations
        self.center_x, self.center_y = 400, 300  # Center of the canvas
        self.loop_size = 250  # Increased size of the figure-eight path

        # Draw the figure-eight path
        self.draw_path()

        # Create the ball
        self.ball = self.canvas.create_oval(
            0, 0, self.ball_size, self.ball_size, fill="yellow"
        )  # Ball is yellow

        # Start animation
        self.animate()

    def draw_path(self):
        """Draw the figure-eight path on the canvas."""
        num_points = 500  # Number of points to create a smooth path
        for i in range(num_points):
            t = i / num_points * (2 * math.pi)  # Parameter for full loop
            x = self.center_x + self.loop_size * math.sin(t)
            y = self.center_y + self.loop_size * math.sin(t) * math.cos(t)
            if i > 0:
                self.canvas.create_line(
                    x_prev, y_prev, x, y, fill="black", width=5  # Thicker line
                )
            x_prev, y_prev = x, y

    def animate(self):
        """Animate the ball along the figure-eight path."""
        # Parametric equations for the figure-eight
        x = self.center_x + self.loop_size * math.sin(self.t)
        y = self.center_y + self.loop_size * math.sin(self.t) * math.cos(self.t)

        # Update ball position
        self.canvas.coords(
            self.ball,
            x - self.ball_size / 2,
            y - self.ball_size / 2,
            x + self.ball_size / 2,
            y + self.ball_size / 2,
        )

        # Increment parameter for movement
        self.t += self.speed
        if self.t >= 2 * math.pi:  # Reset t for continuous looping
            self.t = 0

        # Continue the animation
        self.root.after(16, self.animate)  # Approx. 60 FPS

if __name__ == "__main__":
    root = tk.Tk()
    game = InfinitePathGame(root)
    root.mainloop()
