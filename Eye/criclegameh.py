import tkinter as tk

class EyeImprovementGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Eye Improvement Game")

        # Create canvas
        self.canvas = tk.Canvas(root, width=800, height=600, bg='light green')
        self.canvas.pack()

        # Balls' initial positions (top and bottom horizontal alignment with a larger gap)
        self.top_balls_positions = [(50, 100), (150, 100), (250, 100), (350, 100),
                                     (450, 100), (550, 100), (650, 100), (750, 100)]  # 8 balls at top row
        self.bottom_balls_positions = [(50, 400), (150, 400), (250, 400), (350, 400),
                                        (450, 400), (550, 400), (650, 400), (750, 400)]  # 8 balls at bottom row

        self.top_balls = []
        self.bottom_balls = []

        self.create_balls()

        # Movement flags
        self.current_top_ball_index = 0  # The first top ball to move
        self.current_bottom_ball_index = 0  # The first bottom ball to move
        self.forward_speed = 10  # Initial forward speed of the balls
        self.return_speed = 20  # Initial return speed of the balls

        # Ball movement state
        self.top_ball_moving = True
        self.bottom_ball_moving = False
        self.bottom_ball_returning = False  # Flag to track if bottom balls are returning

        # Start moving the balls
        self.move_balls()

    def create_balls(self):
        """Create balls in two horizontal rows on the top and bottom sides."""
        for pos in self.top_balls_positions:
            x, y = pos
            ball = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill='dark green')
            self.top_balls.append(ball)

        for pos in self.bottom_balls_positions:
            x, y = pos
            ball = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill='dark green')
            self.bottom_balls.append(ball)

    def move_balls(self):
        """Move one ball at a time from the top row, then the bottom row once all top balls finish."""
        
        # Handle the top ball movement
        if self.current_top_ball_index < len(self.top_balls):
            top_ball = self.top_balls[self.current_top_ball_index]
            bottom_ball = self.bottom_balls[self.current_top_ball_index]

            # Get the coordinates of both balls
            x0, y0, x1, y1 = self.canvas.coords(top_ball)
            bx0, by0, bx1, by1 = self.canvas.coords(bottom_ball)

            # Ball movement (top to bottom)
            if self.top_ball_moving:
                # Move the top ball downward with the current forward speed
                dy = self.forward_speed
                self.canvas.move(top_ball, 0, dy)

                # Check if the top ball has reached the bottom row (no collision)
                if y1 >= by0 - 20 and y0 <= by1 + 20 and x0 <= bx1 + 20 and x1 >= bx0 - 20:
                    # Once the top ball reaches the bottom ball's position, stop the top ball and prepare for return
                    self.top_ball_moving = False
                    self.forward_speed += 1  # Increase the forward speed after each ball movement

            # Ball return movement (bottom to top)
            if not self.top_ball_moving:
                # Move the ball back to its starting position with the return speed
                dy = -self.return_speed
                self.canvas.move(top_ball, 0, dy)

                # Reset top ball's position once it has returned
                if y0 <= 100 + 20:  # Reset when the ball reaches its original position
                    self.canvas.coords(top_ball, self.top_balls_positions[self.current_top_ball_index][0] - 20,
                                       100 - 20, self.top_balls_positions[self.current_top_ball_index][0] + 20,
                                       100 + 20)
                    self.current_top_ball_index += 1
                    self.top_ball_moving = True  # Move to the next top ball after returning to its position

        # Handle the bottom ball movement
        if self.current_top_ball_index == len(self.top_balls):
            # Bottom balls only start moving once all top balls have finished
            if not self.bottom_ball_returning and self.current_bottom_ball_index < len(self.bottom_balls):
                bottom_ball = self.bottom_balls[self.current_bottom_ball_index]
                # Move the bottom ball upward with the current forward speed
                x0, y0, x1, y1 = self.canvas.coords(bottom_ball)
                dy = -self.forward_speed
                self.canvas.move(bottom_ball, 0, dy)

                # Once the bottom ball reaches the top side, prepare for return
                if y1 <= 100 + 20:
                    self.canvas.coords(bottom_ball, self.bottom_balls_positions[self.current_bottom_ball_index][0] - 20,
                                       100 - 20, self.bottom_balls_positions[self.current_bottom_ball_index][0] + 20,
                                       100 + 20)
                    self.current_bottom_ball_index += 1

            # Once all bottom balls have moved up, make them return to the bottom
            if self.current_bottom_ball_index == len(self.bottom_balls) and not self.bottom_ball_returning:
                self.bottom_ball_returning = True
                self.current_bottom_ball_index = 0  # Reset to start moving bottom balls again

            # Return the bottom balls to their original positions
            if self.bottom_ball_returning:
                if self.current_bottom_ball_index < len(self.bottom_balls):
                    bottom_ball = self.bottom_balls[self.current_bottom_ball_index]
                    # Move the bottom ball back down with the current return speed
                    x0, y0, x1, y1 = self.canvas.coords(bottom_ball)
                    dy = self.return_speed
                    self.canvas.move(bottom_ball, 0, dy)

                    # Reset bottom ball's position once it has returned
                    if y1 >= self.bottom_balls_positions[self.current_bottom_ball_index][1] + 20:
                        self.canvas.coords(bottom_ball, self.bottom_balls_positions[self.current_bottom_ball_index][0] - 20,
                                           self.bottom_balls_positions[self.current_bottom_ball_index][1] - 20,
                                           self.bottom_balls_positions[self.current_bottom_ball_index][0] + 20,
                                           self.bottom_balls_positions[self.current_bottom_ball_index][1] + 20)
                        self.current_bottom_ball_index += 1

                # Once all bottom balls have returned to their original positions, reset
                if self.current_bottom_ball_index == len(self.bottom_balls):
                    self.bottom_ball_returning = False
                    self.current_bottom_ball_index = 0

        # Repeat movement every 50ms
        self.root.after(50, self.move_balls)

if __name__ == "__main__":
    root = tk.Tk()
    game = EyeImprovementGame(root)
    root.mainloop()
