import tkinter as tk
import random
class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)
        self.snake_pos = [(100, 100), (80, 100), (60, 100)]
        self.food_pos = self.set_new_food_position()
        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press)
        self.load_assets()
        self.create_objects()
        self.after(100, self.perform_actions)
