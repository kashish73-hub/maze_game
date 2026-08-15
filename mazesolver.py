import tkinter as tk
from tkinter import messagebox
import random

# Maze size
ROWS, COLS = 10, 10
CELL_SIZE = 50
root = tk.Tk()
root.title("Maze Solver Game🧩- Backtracking Algorithm")
root.resizable(False, False)
root.configure(bg="#222")

canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="white", highlightthickness=0)
canvas.pack(pady=10)
#Colors
WALL_COLOR = "black"
PATH_COLOR = "white"
START_COLOR = "red"
END_COLOR = "green"
SOLUTION_COLOR = "#1E90FF"
VISITED_COLOR = "#87CEFA"
# Global variables
maze= []
visited = []
path = []
start = (0, 0)
end = (ROWS - 1, COLS - 1)
solved = False

# Generate random maze
def generate_maze():
    global maze, visited, path, solved
    solved = False
    path = []
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]

    # Create a maze with random walls (0 = wall, 1 = path)
    maze = [[random.choice([0, 1, 1, 1]) for _ in range(COLS)] for _ in range(ROWS)]
    maze[start[0]][start[1]] = 1
    maze[end[0]][end[1]] = 1

# Draw maze grid
def draw_maze():
    canvas.delete("all")
    for i in range(ROWS):
        for j in range(COLS):
            x1 = j * CELL_SIZE
            y1 = i * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            color = PATH_COLOR if maze[i][j] == 1 else WALL_COLOR
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    # Mark start & end
    draw_cell(start, START_COLOR)
    draw_cell(end, END_COLOR)

def draw_cell(cell, color):
    i, j = cell
    x1 = j * CELL_SIZE
    y1 = i * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

def is_safe(x, y):
    return 0 <= x < ROWS and 0 <= y < COLS and maze[x][y] == 1 and not visited[x][y]

# Backtracking algorithm
def solve_maze(x, y):
    global solved
    if (x, y) == end:
        path.append((x, y))
        solved = True
        return True

    if is_safe(x, y):
        visited[x][y] = True
        path.append((x, y))
        draw_cell((x, y), VISITED_COLOR)
        root.update()
        root.after(80)

        # Move in 4 directions
        if solve_maze(x + 1, y): return True
        if solve_maze(x, y + 1): return True
        if solve_maze(x - 1, y): return True
        if solve_maze(x, y - 1): return True

        # Backtrack
        path.pop()
        draw_cell((x, y), PATH_COLOR)
        draw_cell(start, START_COLOR)
        draw_cell(end, END_COLOR)
        root.update()
        return False
    return False

def visualize_solution():
    if solve_maze(*start):
        for (i, j) in path:
            if (i, j) != start and (i, j) != end:
                draw_cell((i, j), SOLUTION_COLOR)
                root.update()
                root.after(100)
        messagebox.showinfo("Maze Solver", "✅ Wow!, Maze solved successfully!")
    else:
        messagebox.showerror("Maze Solver", "❌ Soory, No path found!")

# Reset and play again
def reset_game():
    generate_maze()
    draw_maze()

# UI Buttons
frame = tk.Frame(root, bg="#333")
frame.pack(fill="x", pady=5)

solve_btn = tk.Button(frame, text="🧩 Solve Maze", command=visualize_solution,
                      bg="#28A745", fg="white", font=("Arial", 12, "bold"), width=12)
solve_btn.pack(side="left", padx=15, pady=10)

reset_btn = tk.Button(frame, text="🔄 New Maze", command=reset_game,
                      bg="#FFC107", fg="black", font=("Arial", 12, "bold"), width=12)
reset_btn.pack(side="right", padx=15, pady=10)

# Start
generate_maze()
draw_maze()
root.mainloop()
