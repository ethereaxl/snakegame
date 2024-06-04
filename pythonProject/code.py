import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Змейка")
        self.board = None
        self.create_menu()

    def create_menu(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack()
        root.geometry("500x500")

        tk.Label(self.menu_frame, text="Змейка", font=('TkDefaultFont', 24)).pack(pady=10)
        tk.Button(self.menu_frame, text="Начать игру", command=self.start_game).pack(pady=10)
        tk.Button(self.menu_frame, text="Выйти", command=self.root.destroy).pack(pady=10)

    def start_game(self):
        if self.board:
            self.board.destroy()
        self.menu_frame.pack_forget()
        self.board = Snake(self.root, self.end_game)
        self.board.pack()

    def end_game(self, score):
        self.board.pack_forget()
        self.create_menu()
        tk.Label(self.menu_frame, text=f"Ваш счет: {score}", font=('TkDefaultFont', 18)).pack(pady=10)

class Snake(tk.Canvas):
    def __init__(self, root, end_game_callback):
        super().__init__(root, width=600, height=620, background="black", highlightthickness=0)
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
        return (random.randint(0, 29) * 20, random.randint(0, 29) * 20)

    def create_objects(self):
        self.create_text(
            45, 12, text=f"Счет: {self.score}", tag="score", fill="white", font=('TkDefaultFont', 14)
        )
        self.create_snake()
        self.create_food()

    def create_snake(self):
        for x_position, y_position in self.snake_pos:
            self.create_rectangle(
                x_position, y_position, x_position + 20, y_position + 20, fill="green"
            )

    def create_food(self):
        self.create_rectangle(
            self.food_pos[0], self.food_pos[1], self.food_pos[0] + 20, self.food_pos[1] + 20, fill="red"
        )

    def perform_actions(self):
        if self.in_game:
            self.check_collisions()
            self.check_food_collision()
            self.move_snake()
            self.after(100, self.perform_actions)
        else:
            self.end_game()

    def check_collisions(self):
        pass

    def check_food_collision(self):
        pass

    def move_snake(self):
        pass

    def on_key_press(self, e):
        pass

    def end_game(self):
        self.in_game = False
        self.delete(tk.ALL)
        self.end_game_callback(self.score)

root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
