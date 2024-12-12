import tkinter as tk

class EyeTrainingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Eye Tracking Game")
        self.root.geometry("800x600")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="#fefcff")  # Background is soft white
        self.canvas.pack()

        # Initialize variables
        self.ball = None
        self.mode = "zigzag"  # Only "zigzag" mode implemented
        self.ball_size = 30
        self.speed = 0.8  # Adjust speed for ball movement
        self.t = 0
        self.direction = 1  # 1 for forward, -1 for reverse

        # Draw initial path
        self.draw_path()

        # Create ball
        self.ball = self.canvas.create_oval(0, 0, self.ball_size, self.ball_size, fill="red")  # Ball is red

        # Start animation
        self.animate()

        # Add controls
        self.root.bind("<z>", lambda event: self.set_mode("zigzag"))

    def set_mode(self, mode):
        self.mode = mode
        self.t = 0
        self.direction = 1
        self.draw_path()

    def draw_path(self):
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

    def animate(self):
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

        self.root.after(16, self.animate)  # Approx. 60 FPS

if __name__ == "__main__":
    root = tk.Tk()
    game = EyeTrainingGame(root)
    root.mainloop()
