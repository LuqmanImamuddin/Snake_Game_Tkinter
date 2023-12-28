from tkinter import *
import random

# Global Variable
GAME_WIDTH = 700
GAME_HEIGHT = 700
GAME_SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 5
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Snake Class
class Snake:
  def __init__(self):
    self.body_size = BODY_PARTS
    self.coordinates = []
    self.squares = []

    # Snake Starting Position and Amount of Body
    for i in range(0, BODY_PARTS):
      self.coordinates.append([0,0])

    # lukis ular atas canvas (tempat pergerakan ular)
    for x,y  in self.coordinates:
      squares = canvas.create_rectangle(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
      self.squares.append(squares)

# Food Class
class Food:
  def __init__(self):
    x = random.randint(0,(GAME_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE
    y = random.randint(0,(GAME_HEIGHT/SPACE_SIZE) - 1) * SPACE_SIZE
    self.coordinates = [x,y]
    canvas.create_oval(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# fungsi untuk pergerakan ular
def next_turn(snake, food):
  x,y = snake.coordinates[0]

  if direction == "up":
    y -= SPACE_SIZE
  elif direction == "down":
    y += SPACE_SIZE
  elif direction == "left":
    x -= SPACE_SIZE
  elif direction == "right":
    x += SPACE_SIZE

  # masukkan x,y ke snake.coordinates
  snake.coordinates.insert(0, (x,y))
  square = canvas.create_rectangle(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
  snake.squares.insert(0,square)

  # masukkan score kalau langgar food
  if x == food.coordinates[0] and y == food.coordinates[1]:
    global score
    score += 1
    label.config(text="Score: {}".format(score))
    canvas.delete("food")
    food = Food()
  else:
  # padamkan jejak pergerakan tinggalkan jumlah ikut body part sahaja = 3
    del snake.coordinates[-1]
    canvas.delete(snake.squares[-1])
    del snake.squares[-1]

  # semak kalau berlanggar ke idok
  if check_collision(snake):
    game_over()
  else:
    window.after(GAME_SPEED, next_turn, snake, food)

# fungsi untuk ubah pergerakan ular
def change_direction(new_direction):
  global direction

  if new_direction == "left":
    if direction != "right":
      direction = new_direction
  elif new_direction == "right":
    if direction != "left":
      direction = new_direction
  elif new_direction == "up":
    if direction != "down":
      direction = new_direction
  elif new_direction == "down":
    if direction != "up":
      direction = new_direction

# fungsi untuk pelanggaran object dinding dan makanan
def check_collision(snake):
  x,y = snake.coordinates[0]

  if x < 0 or x >= GAME_WIDTH:
    return True
  elif y < 0 or y >= GAME_HEIGHT:
    return True

  for body_parts in snake.coordinates[1:]:
    if x == body_parts[0] and y == body_parts[1]:
      return True

  return False

# fungsi untuk game habis
def game_over():
  canvas.delete(ALL)
  canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")

# fungsi untuk restart game
def restart_game():
    global score, direction, snake, food
    score = 0
    direction = "down"
    label.config(text="Score : {}".format(score))
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    next_turn(snake, food)

# ruangan kod utama
# panggil instant dari tkinter
window = Tk()
# setkan judul window
window.title("Game Ulau")
# buatkan window tak boleh di olah saiznya
window.resizable("False","False")
# setkan score awal
score = 0
# pergerakan awal ular
direction = "down"
# label untuk score pada window game
label = Label(window, text="Score : {}".format(score), font=('consolas',40))
label.pack()
# create restart button
restart_button = Button(window, text="Restart Game", command=restart_game, font=('consolas', 16))
restart_button.pack()
# setkan canvas untuk ular dan makanan bergerak
canvas = Canvas(window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()


# refresh window untuk mulakan game
window.update()
# setkan ruang untuk pergerakan permainan
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
# posisikan window permainan - lebih ketara pada pc compiler
x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)
# setkan geometry window
window.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

# hubungkan kod dengan keyboard untuk gerakkan ular
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

# munculkan ular dan makanan
snake = Snake()
food = Food()

# gerakan ular dan makanan
next_turn(snake, food)

# object untuk pantau pergerakan sepanjang game - listen
window.mainloop()