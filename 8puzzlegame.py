import tkinter as tk
from tkinter import messagebox
import random
from collections import deque
import heapq

class PuzzleGame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("8-Puzzle Game")
        self.geometry("600x600")
        self.board = [[0, 2, 3],
                      [4, 1, 5],
                      [7, 8, 6]]
        self.empty_row = 0
        self.empty_col = 0
        self.steps = 0

        self.create_board()
        self.configure(background="#080808")

        self.bind_arrows()
        self.create_solve_button()

    def create_board(self):
        self.board_frame = tk.Frame(self, width=300, height=300, bg="#080808")
        self.board_frame.pack()
        
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.board_frame, width=8, height=4, font=('Helvetica', 20, 'bold'))
                button.grid(row=i, column=j)
                button.config(command=lambda row=i, col=j: self.move(row, col))
                row.append(button)
            self.buttons.append(row)
        
        self.randomize_button = tk.Button(self, text="Randomize", command=self.randomize,font=('Helvetica', 13, 'bold'),fg="white",width=10, height=2)
        self.randomize_button.pack(pady=11, side=tk.LEFT)
        self.randomize_button.config(bg="black")

        self.steps_counter = tk.Label(self, text="Steps: 0",fg="white",font=('Helvetica', 13, 'bold'),width=10,height=2)
        self.steps_counter.pack(side=tk.RIGHT, padx=10)
        self.steps_counter.config(bg="black")
    
        self.update_buttons()
        
    def create_solve_button(self):
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("Breadth First Search")

        algorithm_label = tk.Label(self, text="Search Algorithm:",font=('Helvetica', 13, 'bold'),fg="white")
        algorithm_label.pack(side=tk.TOP, pady=10)
        algorithm_label.config(bg="black")

        algorithm_combobox = tk.OptionMenu(self, self.algorithm_var, "Breadth First Search", "Depth First Search", "Uniform Cost Search", "A*", "Greedy Search", "Iterative Deepening")
        algorithm_combobox.pack(side=tk.TOP)
        algorithm_combobox.config(bg="black",fg="white",font=('Helvetica', 13, 'bold'))

        solve_button = tk.Button(self, text="Solve", command=self.solve_puzzle,font=('Helvetica', 13, 'bold'),width=10,height=2)
        solve_button.pack(side=tk.TOP, pady=10)

    
    def bind_arrows(self):
        self.bind("<KeyPress-Up>", lambda event: self.move(self.empty_row - 1, self.empty_col))
        self.bind("<KeyPress-Down>", lambda event: self.move(self.empty_row + 1, self.empty_col))
        self.bind("<KeyPress-Left>", lambda event: self.move(self.empty_row, self.empty_col - 1))
        self.bind("<KeyPress-Right>", lambda event: self.move(self.empty_row, self.empty_col + 1))
        self.focus_set()

    def move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[self.empty_row][self.empty_col] = self.board[row][col]
            self.board[row][col] = 0
            self.empty_row = row
            self.empty_col = col
            self.update_buttons()
            
            self.steps += 1
            self.steps_counter.config(text="Steps: " + str(self.steps))

            if self.check_win():
                self.show_win_message()

    def is_valid_move(self, row, col):
        return (row == self.empty_row and (col == self.empty_col - 1 or col == self.empty_col + 1)) or \
               (col == self.empty_col and (row == self.empty_row - 1 or row == self.empty_row + 1))

    def check_win(self):
        goal_state = [[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 0]]
        return self.board == goal_state

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.board[i][j])

    def show_win_message(self):
        messagebox.showinfo("Congratulations!", "You won the game!")

    def randomize(self):
        numbers = list(range(1, 9))
        while True:
            random.shuffle(numbers)
            # Calculate the number of inversions
            inversions = sum(1 for i in range(len(numbers)) for j in range(i+1, len(numbers)) if numbers[i] > numbers[j])
            # If the number of inversions is even, break the loop
            if inversions % 2 == 0:
                break

        index = 0
        for i in range(3):
            for j in range(3):
                if i == self.empty_row and j == self.empty_col:
                    self.board[i][j] = 0
                else:
                    self.board[i][j] = numbers[index]
                    index += 1
                        
        self.update_buttons()


    def solve_puzzle(self):
        start_state = self.get_state()
        algorithm = self.algorithm_var.get()
    
        if algorithm == "Breadth First Search":
            path = self.breadth_first_search(start_state)
        elif algorithm == "Depth First Search":
            path = self.depth_first_search(start_state)
        elif algorithm == "Iterative Deepening":
            path = self.iterative_deepening(start_state)
        elif algorithm == "Uniform Cost Search":
            path = self.uniform_cost_search(start_state)
        elif algorithm == "A*":
            path = self.a_star(start_state)
        elif algorithm == "Greedy Search":
            path = self.greedy_search(start_state)
        else:
            messagebox.showerror("Error", "Invalid search algorithm!")
            return
    
        if path:
            self.animate_solution(path)
        else:
            messagebox.showinfo("No Solution", "No solution found for the given puzzle!")
        
        self.steps = 0  # Reset the step counter
        self.steps_counter.config(text="Steps: 0")  # Update the step counter label

    def get_state(self):
        state = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(self.board[i][j])
            state.append(row)
        return state

    def breadth_first_search(self, start_state):
        queue = deque([(start_state, [])])  # (state, path from start_state)
        visited = set()

        while queue:
            state, path = queue.popleft()

            if state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
                return path

            hashable_state = tuple(tuple(row) for row in state)
            if hashable_state in visited:
                continue

            visited.add(hashable_state)

            row, col = self.find_empty_cell(state)
            neighbors = self.get_neighbors(state, row, col)

            for neighbor, direction in neighbors:
                new_path = path + [direction]
                queue.append((neighbor, new_path))

        return None
    
    def uniform_cost_search(self, start_state):
        priority_queue = [(0, start_state, [])]  # (cost, state, path from start_state)
        visited = set()

        while priority_queue:
            cost, state, path = heapq.heappop(priority_queue)
            
            if state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
                return path
            
            hashable_state = tuple(tuple(row) for row in state)
            if hashable_state in visited:
                continue
            
            visited.add(hashable_state)
            
            row, col = self.find_empty_cell(state)
            neighbors = self.get_neighbors(state, row, col)
            
            for neighbor, direction in neighbors:
                new_cost = cost + 1  # Increment cost by 1 for each move
                new_path = path + [direction]
                heapq.heappush(priority_queue, (new_cost, neighbor, new_path))

        return None

    def iterative_deepening(self, start_state):
        for depth in range(1, 100):  # Set a maximum depth of 100 (can be adjusted as needed)
            result = self.depth_limited_search(start_state, depth)
            if result is not None:
                return result

        return None

    def depth_limited_search(self, state, depth):
        if depth == 0:
            if state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
                return []
            else:
                return None

        row, col = self.find_empty_cell(state)
        neighbors = self.get_neighbors(state, row, col)

        for neighbor, direction in neighbors:
            result = self.depth_limited_search(neighbor, depth - 1)
            if result is not None:
                return [direction] + result

        return None

    
    def greedy_search(self, start_state):
        priority_queue = [(self.h(start_state), start_state, [])]  # (heuristic cost, state, path from start_state)
        visited = set()

        while priority_queue:
            _, state, path = heapq.heappop(priority_queue)
            
            if state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
                return path

            hashable_state = tuple(tuple(row) for row in state)
            if hashable_state in visited:
                continue

            visited.add(hashable_state)

            row, col = self.find_empty_cell(state)
            neighbors = self.get_neighbors(state, row, col)
            
            for neighbor, direction in neighbors:
                new_path = path + [direction]
                heapq.heappush(priority_queue, (self.h(neighbor), neighbor, new_path))

        return None


    def h(self, state):
        # Heuristic function: Manhattan Distance
        goal_state = [[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 0]]
        distance = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != goal_state[i][j]:
                    row, col = self.get_goal_position(state[i][j])
                    distance += abs(i - row) + abs(j - col)
        return distance
    
    def get_goal_position(self, number):
        goal_state = [[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 0]]
        for i in range(3):
            for j in range(3):
                if goal_state[i][j] == number:
                    return i, j
                
    def a_star(self, start_state):
        priority_queue = [(self.h(start_state), 0, start_state, [])] # (heuristic cost, cost, state, path from start_state)
        visited = set()

        while priority_queue:
            _, cost, state, path = heapq.heappop(priority_queue)

            if state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
                return path

            hashable_state = tuple(tuple(row) for row in state)
            if hashable_state in visited:
                continue

            visited.add(hashable_state)

            row, col = self.find_empty_cell(state)
            neighbors = self.get_neighbors(state, row, col)

            for neighbor, direction in neighbors:
                new_cost = cost + 1
                new_path = path + [direction]
                heapq.heappush(priority_queue, (new_cost + self.h(neighbor), new_cost, neighbor, new_path))

        return None
    
    def find_empty_cell(self, state):
        for row in range(3):
            for col in range(3):
                if state[row][col] == 0:
                    return row, col

    def get_neighbors(self, state, row, col):
        neighbors = []
        if row > 0:  # Check upward neighbor
            neighbor = [list(row) for row in state]
            neighbor[row][col] = neighbor[row - 1][col]
            neighbor[row - 1][col] = 0
            neighbors.append((neighbor, "Up"))
        if row < 2:  # Check downward neighbor
            neighbor = [list(row) for row in state]
            neighbor[row][col] = neighbor[row + 1][col]
            neighbor[row + 1][col] = 0
            neighbors.append((neighbor, "Down"))
        if col > 0:  # Check left neighbor
            neighbor = [list(row) for row in state]
            neighbor[row][col] = neighbor[row][col - 1]
            neighbor[row][col - 1] = 0
            neighbors.append((neighbor, "Left"))
        if col < 2:  # Check right neighbor
            neighbor = [list(row) for row in state]
            neighbor[row][col] = neighbor[row][col + 1]
            neighbor[row][col + 1] = 0
            neighbors.append((neighbor, "Right"))
        return neighbors

    def animate_solution(self, path):
        for direction in path:
            if direction == "Up":
                self.move(self.empty_row - 1, self.empty_col)
            elif direction == "Down":
                self.move(self.empty_row + 1, self.empty_col)
            elif direction == "Left":
                self.move(self.empty_row, self.empty_col - 1)
            elif direction == "Right":
                self.move(self.empty_row, self.empty_col + 1)
            self.update()
            self.after(500)

if __name__ == "__main__":
    game = PuzzleGame()
    game.mainloop()