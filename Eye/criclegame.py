import tkinter as tk

class EyeImprovementGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Eye Improvement Game")

        # Create canvas
        self.canvas = tk.Canvas(root, width=800, height=600, bg='light green')
        self.canvas.pack()

        # Balls' initial positions (left and right vertical alignment)
        self.left_balls_positions = [(50, 50), (50, 150), (50, 250), (50, 350)]
        self.right_balls_positions = [(750, 50), (750, 150), (750, 250), (750, 350)]

        self.left_balls = []
        self.right_balls = []

        self.create_balls()

        # Movement flags
        self.current_left_ball_index = 0  # The first left ball to move
        self.current_right_ball_index = 0  # The first right ball to move
        self.forward_speed = 10  # Initial forward speed of the balls
        self.return_speed = 20  # Initial return speed of the balls

        # Ball movement state
        self.left_ball_moving = True
        self.right_ball_moving = False

        # Start moving the balls
        self.move_balls()

    def create_balls(self):
        """Create balls in two vertical alignments on the left and right sides."""
        for pos in self.left_balls_positions:
            x, y = pos
            ball = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill='dark green')
            self.left_balls.append(ball)

        for pos in self.right_balls_positions:
            x, y = pos
            ball = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill='dark green')
            self.right_balls.append(ball)

    def move_balls(self):
        """Move one ball at a time from the left side, then the right side once all left balls finish."""
        # Handle the left ball movement
        if self.current_left_ball_index < len(self.left_balls):
            left_ball = self.left_balls[self.current_left_ball_index]
            right_ball = self.right_balls[self.current_left_ball_index]

            # Get the coordinates of both balls
            x0, y0, x1, y1 = self.canvas.coords(left_ball)
            rx0, ry0, rx1, ry1 = self.canvas.coords(right_ball)

            # Ball movement (left to right)
            if self.left_ball_moving:
                # Move the left ball to the right with the current forward speed
                dx = self.forward_speed
                self.canvas.move(left_ball, dx, 0)

                # Check if the left ball has touched the right ball
                if x1 >= rx0 - 20 and x0 <= rx1 + 20 and y0 <= ry1 + 20 and y1 >= ry0 - 20:
                    # Once the left ball touches the right ball, stop the left ball and prepare for return
                    self.left_ball_moving = False
                    self.forward_speed += 1  # Increase the forward speed after each ball movement

            # Ball return movement (right to left)
            if not self.left_ball_moving:
                # Move the ball back to its starting position with the return speed
                dx = -self.return_speed
                self.canvas.move(left_ball, dx, 0)

                # Reset left ball's position once it has returned
                if x0 <= 50 + 20:
                    # Once the ball reaches its original position, prepare for the next ball
                    self.canvas.coords(left_ball, 50 - 20, self.left_balls_positions[self.current_left_ball_index][1] - 20,
                                       50 + 20, self.left_balls_positions[self.current_left_ball_index][1] + 20)
                    self.current_left_ball_index += 1
                    self.left_ball_moving = True  # Move to the next left ball after returning to its position

        # Once all the left balls have moved, start moving right balls
        if self.current_left_ball_index == len(self.left_balls):
            if self.current_right_ball_index < len(self.right_balls):
                right_ball = self.right_balls[self.current_right_ball_index]
                # Move the right ball to the left with the current forward speed
                x0, y0, x1, y1 = self.canvas.coords(right_ball)
                dx = -self.forward_speed
                self.canvas.move(right_ball, dx, 0)

                # Once the right ball reaches the left side, reset it
                if x1 <= 50 + 20:
                    self.canvas.coords(right_ball, 750 - 20, self.right_balls_positions[self.current_right_ball_index][1] - 20,
                                       750 + 20, self.right_balls_positions[self.current_right_ball_index][1] + 20)
                    self.current_right_ball_index += 1
                    # Check if all right balls have moved and reset if necessary
                    if self.current_right_ball_index == len(self.right_balls):
                        self.current_right_ball_index = 0  # Reset once all right balls are done

        # Repeat movement every 50ms
        self.root.after(50, self.move_balls)

if __name__ == "__main__":
    root = tk.Tk()
    game = EyeImprovementGame(root)
    root.mainloop()
