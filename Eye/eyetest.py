import tkinter as tk
import time
import math  # Import math module

class EyeTrainingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Eye Tracking Game")
        self.root.geometry("800x600")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="#fefcff")  # Background is soft white
        self.canvas.pack()

        # Initialize variables
        self.ball = None
        self.mode = "zigzag"  # Default mode is zigzag
        self.ball_size = 30
        self.speed_zigzag = 0.8  # Starting speed for zigzag mode
        self.speed_star = 0.02  # Starting speed for star mode
        self.speed = self.speed_zigzag  # Default to zigzag speed
        self.t = 0
        self.direction = 1  # 1 for forward, -1 for reverse
        self.last_switch_time = time.time()  # Track last mode switch time
        self.mode_change_interval = 10  # Change mode every 10 seconds

        # Draw initial path
        self.draw_path()

        # Create ball
        self.ball = self.canvas.create_oval(0, 0, self.ball_size, self.ball_size, fill="red")  # Ball is red

        # Start animation
        self.animate()

        # Add controls
        self.root.bind("<z>", lambda event: self.set_mode("zigzag"))
        self.root.bind("<s>", lambda event: self.set_mode("star"))  # Bind 's' key for star mode

        # Speed control (increase/decrease)
        self.root.bind("<Up>", self.increase_speed)  # Bind 'Up' arrow to increase speed
        self.root.bind("<Down>", self.decrease_speed)  # Bind 'Down' arrow to decrease speed

    def set_mode(self, mode):
        """Set the mode and reset parameters accordingly."""
        self.mode = mode
        self.t = 0
        self.direction = 1
        if self.mode == "zigzag":
            self.speed = self.speed_zigzag  # Set zigzag speed
        elif self.mode == "star":
            self.speed = self.speed_star  # Set star speed
        self.draw_path()

    def draw_path(self):
        """Draw path based on the current mode."""
        self.canvas.delete("path")
        if self.mode == "zigzag":
            for i in range(12):  # 12 segments for a full zigzag path
                # Start and end points of each segment
                x1 = 50 + i * 60  # Horizontal position starts at 50, increments by 60 per segment
                y1 = 50 if i % 2 == 0 else 550  # Alternate between top (50) and bottom (550)
                x2 = 50 + (i + 1) * 60
                y2 = 550 if i % 2 == 0 else 50
                self.canvas.create_line(
                    x1, y1, x2, y2, fill="#6c757d", width=5, tags="path"
                )  # Line is a dark gray for good contrast
        elif self.mode == "star":
            # Define the points of the star
            radius = 200
            center_x, center_y = 400, 300
            points = []

            for i in range(5):
                angle = math.radians(i * 144)  # Use math.radians to convert angle to radians
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
        """Animate the ball along the path based on the current mode."""
        # Mode-specific animation logic
        if self.mode == "zigzag":
            segment_length = 60  # Length of one zigzag segment
            total_length = 12 * segment_length  # Total length of zigzag path

            # Update progress
            self.t += self.direction
            progress = (self.t * self.speed)

            # Reverse direction if end of path is reached
            if progress >= total_length or progress <= 0:
                self.direction *= -1

            # Determine current segment and interpolate position
            progress %= total_length
            segment = int(progress // segment_length)
            segment_progress = (progress % segment_length) / segment_length

            # Get start and end points of the segment
            x1 = 50 + segment * segment_length
            y1 = 50 if segment % 2 == 0 else 550
            x2 = 50 + (segment + 1) * segment_length
            y2 = 550 if segment % 2 == 0 else 50

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
        elif self.mode == "star":
            # Star mode animation code (similar to previous example)
            num_points = 5
            radius = 200
            center_x, center_y = 400, 300
            points = []

            for i in range(num_points):
                angle = math.radians(i * 144)  # Use math.radians to convert angle to radians
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

        self.root.after(16, self.animate)  # Approx. 60 FPS

    def switch_mode(self):
        """Switch between modes every 10 seconds."""
        if self.mode == "zigzag":
            self.set_mode("star")  # Switch to star mode
        else:
            self.set_mode("zigzag")  # Switch to zigzag mode

    def increase_speed(self, event):
        """Increase speed for the current mode."""
        if self.mode == "zigzag":
            self.speed_zigzag = min(self.speed_zigzag + 0.01, 2)  # Max speed for zigzag
            self.speed = self.speed_zigzag
        elif self.mode == "star":
            self.speed_star = min(self.speed_star + 0.01, 0.5)  # Max speed for star
            self.speed = self.speed_star
        print(f"Speed increased: {self.speed}")

    def decrease_speed(self, event):
        """Decrease speed for the current mode."""
        if self.mode == "zigzag":
            self.speed_zigzag = max(self.speed_zigzag - 0.01, 0.01)  # Min speed for zigzag
            self.speed = self.speed_zigzag
        elif self.mode == "star":
            self.speed_star = max(self.speed_star - 0.01, 0.01)  # Min speed for star
            self.speed = self.speed_star
        print(f"Speed decreased: {self.speed}")

if __name__ == "__main__":
    root = tk.Tk()
    game = EyeTrainingGame(root)
    root.mainloop()
