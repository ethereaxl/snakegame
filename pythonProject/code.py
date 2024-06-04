import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Змейка")
        self.board = None
        self.create_menu()

    def create_menu(self):
        self.menu_frame = tk.Frame(self.root, background="black", highlightthickness=0)
        self.menu_frame.pack()
        root.geometry("600x620")
        root.config(bg='black')
        tk.Label(self.menu_frame, text="Змейка", font=('TkDefaultFont', 44),bg='black', fg='white').pack(pady=100)
        tk.Button(self.menu_frame, text="Начать игру", command=self.start_game, font=('TkDefaultFont', 30), bg='black', fg='white').pack(pady=10)
        tk.Button(self.menu_frame, text="Выйти", command=self.root.destroy, font=('TkDefaultFont', 30), bg='black', fg='white').pack(pady=10)

    def start_game(self):
        if self.board:
            self.board.destroy()
        self.menu_frame.pack_forget()
        self.board = Snake(self.root, self.end_game)
        self.board.pack()

    def end_game(self, score):
        self.board.pack_forget()
        self.create_menu()
        tk.Label(self.menu_frame, text=f"Ваш счет: {score}", font=('TkDefaultFont', 18), bg='black', fg='white').pack(pady=10)

class Snake(tk.Canvas):
    def __init__(self, root, end_game_callback):
        super().__init__(root, width=600, height=620, background="black", highlightthickness=0)
        self.paused = False
        self.pause_text = self.create_text(
            300, 310, text="ПАУЗА", font=('TkDefaultFont', 48), fill='white', state='hidden'
        )
        self.end_game_callback = end_game_callback
        self.snake_pos = [(100, 100), (80, 100), (60, 100)]
        self.food_pos = self.set_new_food_position()
        self.direction = "Right"
        self.score = 0
        self.in_game = True
        self.bind_all("<Key>", self.on_key_press)
        self.create_objects()
        self.after(100, self.perform_actions)

    def set_new_food_position(self):
        while True:
            position = (random.randint(0, 29) * 20, random.randint(0, 29) * 20)
            if position not in self.snake_pos:
                return position

    def create_objects(self):
        self.create_text(
            45, 12, text=f"Счет: {self.score}", tag="score", fill="white", font=('TkDefaultFont', 14)
        )
        self.create_snake()
        self.create_food()

    def create_snake(self):
        self.delete("snake")
        for x_position, y_position in self.snake_pos:
            self.create_rectangle(
                x_position, y_position, x_position + 20, y_position + 20, fill="green", tags="snake"
            )

    def create_food(self):
        self.delete("food")
        self.create_rectangle(
            self.food_pos[0], self.food_pos[1], self.food_pos[0] + 20, self.food_pos[1] + 20, fill="red", tags="food"
        )

    def perform_actions(self):
        if self.in_game and not self.paused:
            self.check_collisions()
            self.check_food_collision()
            self.move_snake()
            self.create_snake()
            self.after(100, self.perform_actions)
        elif not self.in_game:
            self.end_game()
        elif self.paused:
            self.itemconfig(self.pause_text, state='normal')

    def check_collisions(self):
        head_x, head_y = self.snake_pos[0]
        if head_x < 0 or head_x >= 600 or head_y < 0 or head_y >= 600 or (head_x, head_y) in self.snake_pos[1:]:
            self.in_game = False

    def check_food_collision(self):
        if self.snake_pos[0] == self.food_pos:
            self.score += 1
            self.snake_pos.append(self.snake_pos[-1])
            self.food_pos = self.set_new_food_position()
            self.create_food()
            self.itemconfig("score", text=f"Счет: {self.score}")

    def move_snake(self):
        head_x, head_y = self.snake_pos[0]
        new_head_pos = ()
        if self.direction == "Left":
            new_head_pos = (head_x - 20, head_y)
        elif self.direction == "Right":
            new_head_pos = (head_x + 20, head_y)
        elif self.direction == "Up":
            new_head_pos = (head_x, head_y - 20)
        elif self.direction == "Down":
            new_head_pos = (head_x, head_y + 20)

        self.snake_pos = [new_head_pos] + self.snake_pos[:-1]

    def on_key_press(self, e):
        new_direction = e.keysym
        if new_direction == "space":
            self.paused = not self.paused
            if not self.paused:
                self.itemconfig(self.pause_text, state='hidden')
                self.perform_actions()
            else:
                self.itemconfig(self.pause_text, state='normal')
        else:
            opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
            if (
                new_direction in opposites and
                opposites[new_direction] != self.direction and
                not self.paused
            ):
                self.direction = new_direction

    def end_game(self):
        self.in_game = False
        self.delete(tk.ALL)
        self.end_game_callback(self.score)

root = tk.Tk()
game = SnakeGame(root)
root.mainloop()