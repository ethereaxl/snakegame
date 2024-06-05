import tkinter as tk
import random
import time
import pygame
class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Змейка")
        self.board = None
        self.total_score = 0
        self.best_times = {1: float('0'), 2: float('0'), 3: float('0')}
        pygame.mixer.init()
        self.bg_music = 'background.mp3'
        self.food_sound = 'eat.mp3'
        self.death_sound = 'gameover.mp3'
        pygame.mixer.music.load(self.bg_music)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.create_menu()

    def create_menu(self):
        self.menu_frame = tk.Frame(self.root, background="black", highlightthickness=0)
        self.menu_frame.pack()
        self.root.geometry("600x620")
        self.root.config(bg='black')
        tk.Label(self.menu_frame, text="Змейка", font=('TkDefaultFont', 44), bg='black', fg='white').pack(pady=50)
        self.create_level_button("Уровень 1", 1)
        self.create_level_button("Уровень 2", 2)
        self.create_level_button("Уровень 3", 3)
        tk.Button(self.menu_frame, text="Выйти", command=self.root.destroy, font=('TkDefaultFont', 23), bg='black', fg='white').pack(pady=12)

    def create_level_button(self, text, level):
        frame = tk.Frame(self.menu_frame, bg='black')
        frame.pack(pady=10, fill='x')
        button = tk.Button(frame, text=text, command=lambda: self.start_game(level), font=('TkDefaultFont', 25), bg='black', fg='white')
        button.pack(side='left', padx=10)
        best_time = self.best_times[level]
        time_text = f"{best_time:.2f} сек"
        tk.Label(frame, text=f"Лучшее время: {time_text}", font=('TkDefaultFont', 16), bg='black', fg='white').pack(side='left', padx=10)

    def start_game(self, level):
        if self.board:
            self.board.destroy()
        self.menu_frame.pack_forget()
        self.board = Snake(self.root, self.end_game, level, self.food_sound, self.death_sound)
        self.board.pack()

    def end_game(self, score, level, time_spent):
        self.total_score += score
        self.best_times[level] = max(self.best_times[level], time_spent)
        self.board.pack_forget()
        self.create_menu()
        tk.Label(self.menu_frame, text=f"Общий счет: {self.total_score}", font=('TkDefaultFont', 16), bg='black',fg='white').pack(pady=10)
        tk.Label(self.menu_frame, text=f"Ваш счет: {score}", font=('TkDefaultFont', 16), bg='black', fg='white').pack(pady=10)
        tk.Label(self.menu_frame, text=f"Время: {time_spent:.2f} сек", font=('TkDefaultFont', 16), bg='black',fg='white').pack(pady=10)


class Snake(tk.Canvas):
    def __init__(self, root, end_game_callback, level, food_sound, death_sound):
        super().__init__(root, width=600, height=620, background="black", highlightthickness=0)
        self.level = level
        self.obstacles = []
        self.paused = False
        self.pause_text = self.create_text(300, 310, text="ПАУЗА", font=('TkDefaultFont', 48), fill='white', state='hidden')
        self.end_game_callback = end_game_callback
        self.snake_pos = [(100, 100), (80, 100), (60, 100)]
        self.food_pos = self.set_new_food_position()
        self.direction = "Right"
        self.score = 0
        self.in_game = True
        self.start_time = time.time()
        self.food_sound = pygame.mixer.Sound(food_sound)
        self.death_sound = pygame.mixer.Sound(death_sound)
        self.bind_all("<Key>", self.on_key_press)
        self.create_objects()
        speed = 100 if level == 1 else 80 if level == 2 else 66
        self.after(speed, self.perform_actions)

    def set_new_food_position(self):
        while True:
            position = (random.randint(0, 29) * 20, random.randint(0, 29) * 20)
            if position not in self.snake_pos and position not in self.obstacles:
                return position

    def create_objects(self):
        self.create_text(45, 12, text=f"Счет: {self.score}", tag="score", fill="white", font=('TkDefaultFont', 14))
        self.create_text(505, 12, text=f"Время: 0.00 сек", tag="timer", fill="white", font=('TkDefaultFont', 14))
        self.create_snake()
        self.create_food()
        if self.level > 1:
            self.create_obstacles()

    def create_snake(self):
        self.delete("snake")
        color = "green" if self.level < 3 else "purple"
        for x_position, y_position in self.snake_pos:
            self.create_rectangle(x_position, y_position, x_position + 20, y_position + 20, fill=color, tags="snake")

    def create_food(self):
        self.delete("food")
        self.create_rectangle(self.food_pos[0], self.food_pos[1], self.food_pos[0] + 20, self.food_pos[1] + 20, fill="red", tags="food")

    def create_obstacles(self):
        self.delete("obstacle")
        num_obstacles = 5 if self.level == 2 else 10
        obstacle_positions = [(random.randint(0, 29) * 20, random.randint(0, 29) * 20) for _ in range(num_obstacles)]
        for pos in obstacle_positions:
            obstacle_area = [(pos[0] + i * 20, pos[1]) for i in range(random.randint(1, 5))]
            self.obstacles.extend(obstacle_area)
            for x_position, y_position in obstacle_area:
                self.create_rectangle(x_position, y_position, x_position + 20, y_position + 20, fill="grey", tags="obstacle")

    def perform_actions(self):
        if self.in_game and not self.paused:
            self.check_collisions()
            self.check_food_collision()
            self.move_snake()
            self.create_snake()
            self.update_timer()
            speed = 100 if self.level == 1 else 80 if self.level == 2 else 66
            self.after(speed, self.perform_actions)
        elif not self.in_game:
            self.end_game()
        elif self.paused:
            self.itemconfig(self.pause_text, state='normal')

    def check_collisions(self):
        head_x, head_y = self.snake_pos[0]
        if head_x < 0 or head_x >= 600 or head_y < 0 or head_y >= 600 or (head_x, head_y) in self.snake_pos[1:] or (
        head_x, head_y) in self.obstacles:
            self.in_game = False
            pygame.mixer.Sound.play(self.death_sound)

    def check_food_collision(self):
        if self.snake_pos[0] == self.food_pos:
            self.score += 1
            self.snake_pos.append(self.snake_pos[-1])
            self.food_pos = self.set_new_food_position()
            self.create_food()
            self.itemconfig("score", text=f"Счет: {self.score}")
            pygame.mixer.Sound.play(self.food_sound)

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

    def update_timer(self):
        current_time = time.time()
        time_spent = current_time - self.start_time
        self.itemconfig("timer", text=f"Время: {time_spent:.2f} сек")

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
            if new_direction in opposites and opposites[new_direction] != self.direction and not self.paused:
                self.direction = new_direction

    def end_game(self):
        self.in_game = False
        time_spent = time.time() - self.start_time
        self.delete(tk.ALL)
        self.end_game_callback(self.score, self.level, time_spent)


root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
