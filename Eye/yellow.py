import tkinter as tk

class GraphVisualization:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Visualization")
        
        # Increase the size of the canvas
        self.canvas_width = 1000
        self.canvas_height = 800
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")  # Increased canvas size
        self.canvas.pack()

        # Updated Node positions to match a larger graph
        # Node positions are adjusted relative to the center of the canvas
        self.node_radius = 40
        self.nodes = [
            (150, 150), (300, 150), (450, 150), (600, 150),
            (150, 300), (300, 300), (450, 300), (600, 300),
            (150, 450), (300, 450), (450, 450), (600, 450)
        ]
        
        # Find center of the canvas
        self.canvas_center_x = self.canvas_width / 2
        self.canvas_center_y = self.canvas_height / 2
        
        # Center the nodes
        self.nodes = [
            (self.canvas_center_x + (x - 375), self.canvas_center_y + (y - 300))
            for (x, y) in self.nodes
        ]

        # Edges connecting the nodes (fixed)
        self.edges = [
            (0, 1), (1, 4), (4, 5), (5, 2), (2, 3),  # Top line
            (3, 6), (6, 7), (8, 6),  # Left connections
            (7, 11), (11, 6), (6, 9), (9, 4), (4, 8), (8, 5), (10, 7)  # Right connections
        ]

        # Create the nodes and edges
        self.create_graph()

        # Index to track which node is yellow
        self.yellow_node_index = 0

        # Start animation
        self.animate()

    def create_graph(self):
        # Draw edges (lines between nodes)
        for edge in self.edges:
            x1, y1 = self.nodes[edge[0]]
            x2, y2 = self.nodes[edge[1]]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=3)

        # Draw nodes (circles) initially set to yellow
        self.circles = []
        for i, (x, y) in enumerate(self.nodes):
            circle = self.canvas.create_oval(
                x - self.node_radius, y - self.node_radius, x + self.node_radius, y + self.node_radius,  # Circle dimensions
                fill="yellow", outline="black", width=3
            )
            self.circles.append(circle)

    def animate(self):
        # Change the current yellow circle to yellow
        self.canvas.itemconfig(self.circles[self.yellow_node_index], fill="yellow")

        # Update the yellow circle index
        self.yellow_node_index = (self.yellow_node_index + 1) % len(self.nodes)

        # Set the next circle to blue
        self.canvas.itemconfig(self.circles[self.yellow_node_index], fill="blue")

        # Call the animate method again after 1000 ms (1 second)
        self.root.after(1000, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphVisualization(root)
    root.mainloop()
