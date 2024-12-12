import tkinter as tk

class ZigzagPathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Zigzag Path Game")
        self.root.geometry("800x600")
        self.canvas = tk.Canvas(root, width=800, height=800, bg="white")  # White background
        self.canvas.pack()

        # Initialize variables
        self.ball_size = 30
        self.speed = 0.8  # Adjust speed for ball movement
        self.t = 0
        self.direction = 1  # 1 for forward, -1 for reverse
        self.num_cycles = 3  # Number of full up and down cycles
        self.segment_length = 60  # Length of one zigzag segment
        self.total_length = 12 * self.segment_length  # Total length of zigzag path (12 segments)

        # Draw the zigzag path
        self.draw_zigzag_path()

        # Create ball
        self.ball = self.canvas.create_oval(0, 0, self.ball_size, self.ball_size, fill="blue")  # Ball is blue

        # Start animation
        self.animate()

    def draw_zigzag_path(self):
        """Draws the zigzag path from top to bottom."""
        self.canvas.delete("path")
        self.path_points = []  # To store the zigzag points for movement
        num_segments = 12  # Number of zigzag segments
        segment_height = 50  # Height of each zigzag segment
        left_x = 100  # Left x-coordinate for the zigzag
        right_x = 700  # Right x-coordinate for the zigzag

        # Generate points for the zigzag path
        for i in range(num_segments + 1):
            x = left_x if i % 2 == 0 else right_x
            y = 50 + i * segment_height
            self.path_points.append((x, y))
            if i > 0:  # Draw line between consecutive points
                self.canvas.create_line(
                    self.path_points[i - 1][0], self.path_points[i - 1][1],
                    x, y, fill="black", width=2, tags="path"
                )

    def animate(self):
        """Animates the ball along the zigzag path for three full up and down cycles."""
        # Update progress
        self.t += self.direction * self.speed
        progress = self.t

        # Reverse direction if the ball reaches the end or the start of the path
        if progress >= self.total_length or progress <= 0:
            self.direction *= -1
            if abs(self.t) > self.num_cycles * self.total_length:
                self.t = 0  # Reset after completing 3 full cycles

        # Calculate the current segment and interpolate position
        num_segments = len(self.path_points) - 1
        segment_length = self.total_length / num_segments

        # Ensure that the current_segment is within valid range
        current_segment = int(progress // segment_length)
        current_segment = max(0, min(current_segment, num_segments - 1))  # Clamp to valid range

        segment_progress = (progress % segment_length) / segment_length

        # Get the start and end points of the current segment
        x1, y1 = self.path_points[current_segment]
        
        # Check if the next segment is within bounds
        if current_segment + 1 < len(self.path_points):
            x2, y2 = self.path_points[current_segment + 1]
        else:
            x2, y2 = x1, y1  # Prevent out-of-bounds error by staying on the last point

        # Interpolate the ball's position along the current segment
        x = x1 + (x2 - x1) * segment_progress
        y = y1 + (y2 - y1) * segment_progress

        # Update ball position
        self.canvas.coords(
            self.ball,
            x - self.ball_size / 2,
            y - self.ball_size / 2,
            x + self.ball_size / 2,
            y + self.ball_size / 2,
        )

        # Schedule the next animation frame
        self.root.after(16, self.animate)  # ~60 FPS

if __name__ == "__main__":
    root = tk.Tk()
    game = ZigzagPathGame(root)
    root.mainloop()
