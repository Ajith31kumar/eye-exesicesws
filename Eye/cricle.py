import tkinter as tk
import math

class CircularPathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Circular Path Game")
        self.root.geometry("800x600")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        # Initialize variables
        self.circle_radius = 200  # Radius of the circular path
        self.center_x, self.center_y = 400, 300  # Center of the circle
        self.angle = 0  # Start angle (top of the circle)
        self.speed = 0.05  # Speed of the ball
        self.small_circle_radius = 40  # Radius for the small circle (instead of red ball)
        self.green_ball_radius = 15  # Radius for green ball
        self.direction = 1  # 1 for clockwise, -1 for counterclockwise

        # Draw the circular path
        self.canvas.create_oval(
            self.center_x - self.circle_radius,
            self.center_y - self.circle_radius,
            self.center_x + self.circle_radius,
            self.center_y + self.circle_radius,
            outline="black",
            width=3,  # Thickness of the circular path
        )

        # Create a new circle at the top of the circular path (where the red ball was)
        self.red_circle_x = self.center_x
        self.red_circle_y = self.center_y - self.circle_radius
        self.canvas.create_oval(
            self.red_circle_x - self.small_circle_radius,
            self.red_circle_y - self.small_circle_radius,
            self.red_circle_x + self.small_circle_radius,
            self.red_circle_y + self.small_circle_radius,
            outline="black",  # Optional: Can change color of the new circle
            width=3,  # Optional: You can set the border width if you want
        )

        # Create the green moving ball
        self.green_ball = self.canvas.create_oval(
            self.red_circle_x - self.green_ball_radius,
            self.red_circle_y - self.green_ball_radius,
            self.red_circle_x + self.green_ball_radius,
            self.red_circle_y + self.green_ball_radius,
            fill="green",
        )

        # Start the animation
        self.animate()

    def animate(self):
        # Update the angle based on speed and direction
        self.angle += self.speed * self.direction

        # Normalize the angle to stay within [0, 2π] (full circle)
        if self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi
        elif self.angle < 0:
            self.angle += 2 * math.pi

        # Calculate the current position of the green ball
        x = self.center_x + self.circle_radius * math.cos(self.angle)
        y = self.center_y + self.circle_radius * math.sin(self.angle)

        # Update the position of the green ball
        self.canvas.coords(
            self.green_ball,
            x - self.green_ball_radius,
            y - self.green_ball_radius,
            x + self.green_ball_radius,
            y + self.green_ball_radius,
        )

        # Check if the green ball is at the top (where the circle is)
        if abs(x - self.red_circle_x) < 1 and abs(y - self.red_circle_y) < 1:
            self.direction *= -1  # Reverse direction every time it touches the circle

        # Continue the animation in a loop
        self.root.after(16, self.animate)  # Approx. 60 FPS

if __name__ == "__main__":
    root = tk.Tk()
    game = CircularPathGame(root)
    root.mainloop()
