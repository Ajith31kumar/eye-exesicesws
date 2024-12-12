import tkinter as tk
import math

class EyeTrainingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Eye Tracking Star Game")
        self.root.geometry("800x600")  
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        # Initialize variables
        self.ball = None
        self.mode = "star"  # Default mode
        self.ball_size = 30
        self.speed = 0.05  # Adjust speed for visible movement
        self.t = 0
        self.direction = 1  # 1 for forward, -1 for reverse

        # Draw initial path
        self.draw_path()

        # Create ball
        self.ball = self.canvas.create_oval(0, 0, self.ball_size, self.ball_size, fill="red")

        # Start animation
        self.animate()

        # Add controls
        self.root.bind("<s>", lambda event: self.set_mode("star"))  # Press 's' to reset to star mode
        self.root.bind("<Up>", self.increase_speed)  # Press 'Up' arrow to increase speed
        self.root.bind("<Down>", self.decrease_speed)  # Press 'Down' arrow to decrease speed

    def set_mode(self, mode):
        self.mode = mode
        self.t = 0
        self.direction = 1
        self.draw_path()

    def draw_path(self):
        self.canvas.delete("path")
        if self.mode == "star":
            # Define the points of the star
            radius = 200
            center_x, center_y = 400, 300
            points = []

            for i in range(5):
                angle = math.radians(i * 144)
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))

            # Draw the star shape
            for i in range(len(points)):
                self.canvas.create_line(
                    points[i][0], points[i][1], 
                    points[(i + 1) % len(points)][0], points[(i + 1) % len(points)][1],
                    fill="black", width=5, tags="path"
                ) 

    def animate(self):
        if self.mode == "star":
            num_points = 5
            radius = 200
            center_x, center_y = 400, 300
            points = []

            # Calculate the star points
            for i in range(num_points):
                angle = math.radians(i * 144)
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))

            # Update progress
            self.t += self.direction * self.speed
            progress = self.t

            # Reverse direction if end of path is reached
            if progress >= num_points or progress < 0:
                self.direction *= -1
                progress = max(0, min(progress, num_points - 1))

            # Determine current segment and interpolate position
            segment = int(progress) % num_points
            segment_progress = progress - segment

            # Get the two points for the current segment
            x1, y1 = points[segment]
            x2, y2 = points[(segment + 1) % num_points]

            # Interpolate position
            x = x1 + (x2 - x1) * segment_progress
            y = y1 + (y2 - y1) * segment_progress

            self.canvas.coords(
                self.ball,
                x - self.ball_size / 2,
                y - self.ball_size / 2,
                x + self.ball_size / 2,
                y + self.ball_size / 2,
            )

        self.root.after(16, self.animate)

    def increase_speed(self, event):
        """Increase the ball's speed."""
        self.speed = min(self.speed + 0.01, 0.2)  # Set an upper limit for speed

    def decrease_speed(self, event):
        """Decrease the ball's speed."""
        self.speed = max(self.speed - 0.01, 0.01)  # Set a lower limit for speed

if __name__ == "__main__":
    root = tk.Tk()
    game = EyeTrainingGame(root)
    root.mainloop()
