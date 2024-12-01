import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game | UlugbekWeb")
        self.canvas = tk.Canvas(root, width=600, height=400, bg="black")
        self.canvas.pack()

        self.snake = [(100, 100), (90, 100), (80, 100)]  # Snake initial position
        self.food = self.spawn_food()
        self.direction = "Right"
        self.score = 0

        self.running = True
        self.create_objects()
        self.root.bind("<KeyPress>", self.change_direction)
        self.update()

    def create_objects(self):
        self.snake_body = [
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green")
            for x, y in self.snake
        ]
        self.food_item = self.canvas.create_rectangle(
            self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red"
        )
        self.score_text = self.canvas.create_text(
            50, 10, text=f"Score: {self.score}", fill="white", font=("Arial", 14)
        )

    def update(self):
        if self.running:
            self.move_snake()
            self.check_collision()
            self.root.after(100, self.update)

    def move_snake(self):
        x, y = self.snake[0]
        if self.direction == "Right":
            x += 10
        elif self.direction == "Left":
            x -= 10
        elif self.direction == "Down":
            y += 10
        elif self.direction == "Up":
            y -= 10
        new_head = (x, y)

        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.canvas.delete(self.food_item)
            self.food = self.spawn_food()
            self.food_item = self.canvas.create_rectangle(
                self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red"
            )
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        else:
            self.snake.insert(0, new_head)
            tail = self.snake.pop()
            self.canvas.delete(self.snake_body[-1])
            self.snake_body.pop()

        # Add new head
        self.snake_body.insert(
            0,
            self.canvas.create_rectangle(
                new_head[0], new_head[1], new_head[0] + 10, new_head[1] + 10, fill="green"
            ),
        )

    def change_direction(self, event):
        if event.keysym in ["Left", "Right", "Up", "Down"]:
            new_direction = event.keysym
            opposite_directions = {
                "Left": "Right",
                "Right": "Left",
                "Up": "Down",
                "Down": "Up",
            }
            if new_direction != opposite_directions.get(self.direction):
                self.direction = new_direction

    def check_collision(self):
        x, y = self.snake[0]
        # Check wall collision
        if x < 0 or y < 0 or x >= 600 or y >= 400:
            self.game_over()
        # Check self collision
        if (x, y) in self.snake[1:]:
            self.game_over()

    def game_over(self):
        self.running = False
        self.canvas.create_text(
            300, 200, text="Game Over", fill="red", font=("Arial", 24)
        )

    def spawn_food(self):
        while True:
            x = random.randint(0, 59) * 10
            y = random.randint(0, 39) * 10
            if (x, y) not in self.snake:
                return x, y


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
