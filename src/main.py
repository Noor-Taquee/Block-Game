from tkinter import Tk, Frame, Label, Button, NSEW
from random import randint
from time import time

window = Tk()
window.geometry("300x500")
window.config(bg="black")
window.focus_set()


# VARIABLES=================================
fg_color = "red"
bg_color = "red"

bonus_duration = 5
bonus_scoreInterval = 50
bonus_scoreIncrement = 20
bonus_currentScore = 0
bonus_startingTime = 0.0
bonus_onGoing = False

pause_startingTime = 0.0

gameStarted = False
pause = False
gameOver = False

score = 0
score_increment = 10

speed = {"easy": 400, "medium": 150, "hard": 50}
difficulty = "easy"
direction = "right"

grid_columns = 13
grid_rows = 20

block_defaultColumn = 0
block_defaultRow = 0

block_column = block_defaultColumn
block_row = block_defaultRow
target_column = None
target_row = None
bonus_column = None
bonus_row = None


# region FUNCTIONS
def move_block():
  global \
    score, \
    block_column, \
    block_row, \
    bonus_currentScore, \
    bonus_startingTime, \
    bonus_onGoing
  if not pause and not gameOver:
    if score % bonus_scoreInterval == 0 and score != bonus_currentScore:
      spawn_bonus()
      bonus_startingTime = time()
      bonus_onGoing = True
      bonus_currentScore = score
    if direction == "up":
      if block_row > 0:
        block_row -= 1
      else:
        game_over()
    elif direction == "down":
      if block_row < grid_rows:
        block_row += 1
      else:
        game_over()
    elif direction == "right":
      if block_column < grid_columns:
        block_column += 1
      else:
        game_over()
    elif direction == "left":
      if block_column > 0:
        block_column -= 1
      else:
        game_over()
    if block_column == target_column and block_row == target_row:
      score += score_increment
      score_display.config(text=f"Score: {score}")
      target.grid_forget()
      spawn_target()
    if bonus_onGoing:
      current_time = time()
      if current_time - bonus_startingTime >= bonus_duration:
        bonus.grid_forget()
        bonus_onGoing = False
      elif block_column == bonus_column and block_row == bonus_row:
        score += bonus_scoreIncrement
        score_display.config(text=f"Score: {score}")
        bonus.grid_forget()
        bonus_onGoing = False
    block.grid(column=block_column, row=block_row, sticky=NSEW)
    block.after(speed[difficulty], move_block)


def spawn_target():
  global target_column, target_row, bonus_column, bonus_row
  while True:
    target_column = randint(0, grid_columns)
    target_row = randint(0, grid_rows)
    if (block_column != target_column or block_row != target_row) and (
      bonus_column != target_column or bonus_row != target_row
    ):
      break
  target.grid(column=target_column, row=target_row, sticky=NSEW)


def spawn_bonus():
  global bonus_column, bonus_row, target_column, target_row
  while True:
    bonus_column = randint(0, grid_columns)
    bonus_row = randint(0, grid_rows)
    if (block_column != bonus_column or block_row != bonus_row) and (
      target_column != bonus_column or target_row != bonus_row
    ):
      break
  bonus.grid(column=bonus_column, row=bonus_row, sticky=NSEW)
  glow(bonus)


def game_over():
  global gameOver
  gameOver = True
  block.config(fg="white", bg="white")
  target.grid_forget()
  bonus.grid_forget()
  score_result.config(text=f"Score: {score}")
  result_panel.grid(column=2, row=7, rowspan=6, columnspan=10, sticky=NSEW)
  window.bind("<Return>", f_reset)


def glow(widget):
  global fg_color, bg_color
  fg_color = "red" if fg_color == "blue" else "blue"
  bg_color = "red" if bg_color == "blue" else "blue"
  widget.config(fg=fg_color, bg=bg_color)
  widget.after(300, glow, widget)


# BUTTON FUNCTIONS=========================
def f_difficulty():
  difficulty_panel.grid(column=0, row=1, sticky=NSEW)


def f_easy():
  global difficulty
  difficulty = "easy"
  bn_difficulty.config(text=f"Difficulty: {difficulty}", fg="green")
  difficulty_panel.grid_forget()


def f_medium():
  global difficulty
  difficulty = "medium"
  bn_difficulty.config(text=f"Difficulty: {difficulty}", fg="orange")
  difficulty_panel.grid_forget()


def f_hard():
  global difficulty
  difficulty = "hard"
  bn_difficulty.config(text=f"Difficulty: {difficulty}", fg="red")
  difficulty_panel.grid_forget()


def f_play(event=None):
  global gameStarted
  if not gameStarted:
    gameStarted = True
    window.bind("<Return>", f_resume)
    start_panel.destroy()
    bn_play.destroy()
    playing_tab.pack(fill="both", expand=True)
    block.grid(column=block_column, row=block_row, sticky=NSEW)
    spawn_target()
    move_block()


def f_option(event=None):
  global pause, pause_startingTime
  if not gameOver and not pause:
    if bonus_onGoing:
      pause_startingTime = time()
    pause = True
    option_panel.grid(column=4, row=5, columnspan=6, rowspan=10, sticky=NSEW)
    option_panel.lift()
    window.bind("<Right>", f_fd)
    window.bind("<Left>", f_bk)
    window.bind("<Return>", f_resume)


def f_resume(event=None):
  global pause, bonus_startingTime
  if pause:
    window.bind("<Right>", f_right)
    window.bind("<Left>", f_left)
    option_panel.grid_forget()
    pause = False
    if bonus_onGoing:
      current_time = time()
      pause_duration = current_time - pause_startingTime
      bonus_startingTime += pause_duration
    move_block()


def f_reset(event=None):
  global \
    pause, \
    gameOver, \
    score, \
    block_column, \
    block_row, \
    direction, \
    bonus_currentScore, \
    bonus_onGoing
  window.unbind("<Return>")
  if pause:
    pause = False
    option_panel.grid_forget()
  elif gameOver:
    gameOver = False
    result_panel.grid_forget()
    block.config(fg="black", bg="black")
  if bonus_onGoing:
    bonus.grid_forget()
    bonus_onGoing = False
  direction = "right"
  score, bonus_currentScore = 0, 0
  block_column, block_row = block_defaultColumn, block_defaultRow
  score_display.config(text=f"Score: {score}")
  block.grid(column=block_column, row=block_row, sticky=NSEW)
  spawn_target()
  move_block()


def f_fd(event=None):
  global difficulty
  if difficulty == "medium":
    difficulty = "hard"
  else:
    difficulty = "medium"
  difficulty_option.config(text=difficulty)


def f_bk(event=None):
  global difficulty
  if difficulty == "medium":
    difficulty = "easy"
  else:
    difficulty = "medium"
  difficulty_option.config(text=difficulty)


def f_up(event=None):
  global direction
  direction = "up"


def f_down(event=None):
  global direction
  direction = "down"


def f_left(event=None):
  global direction
  direction = "left"


def f_right(event=None):
  global direction
  direction = "right"


# endregion FUNCTIONS

# region FRAMES
start_tab = Frame(window)
start_tab.columnconfigure(0, weight=1)

start_panel = Frame(window)
start_panel.columnconfigure(0, weight=1)

bn_difficulty = Button(
  start_panel,
  text=f"Difficulty: {difficulty}",
  fg="green",
  bg="white",
  command=f_difficulty,
)

bn_play = Button(
  start_tab,
  text="PLAY",
  font=("times new roman", 20, "bold"),
  fg="black",
  bg="white",
  command=f_play,
)


# region difficulty panel
difficulty_panel = Frame(start_tab)
difficulty_panel.columnconfigure(0, weight=1)

bn_easy = Button(difficulty_panel, text="easy", fg="white", bg="green", command=f_easy)
bn_medium = Button(
  difficulty_panel, text="medium", fg="white", bg="orange", command=f_medium
)
bn_hard = Button(difficulty_panel, text="hard", fg="white", bg="red", command=f_hard)

# endregion difficulty panel

playing_tab = Frame(window)
playing_tab.columnconfigure(0, weight=1)
playing_tab.rowconfigure(0, weight=1)
playing_tab.rowconfigure(1, weight=200)
playing_tab.rowconfigure(2, weight=1)

# region top bar
top_panel = Frame(playing_tab, bg="black")
for i in range(4):
  top_panel.columnconfigure(i, weight=1)

score_display = Label(
  top_panel,
  text=f"Score: {score}",
  font=("times new roman", 15),
  fg="white",
  bg="black",
)
# endregion top bar

# region area
area_frame = Frame(playing_tab, bg="white")
for i in range(14):
  area_frame.columnconfigure(i, weight=1)
for i in range(21):
  area_frame.rowconfigure(i, weight=1)


block = Label(area_frame, text="", font=("arial", 1), fg="black", bg="black")

target = Label(area_frame, text="", font=("arial", 1), fg="red", bg="red")

bonus = Label(area_frame, text="", font=("arial", 1), fg="red", bg="red")

# endregion area

# region buttons
buttons_panel = Frame(playing_tab, bg="grey")
for i in range(3):
  buttons_panel.columnconfigure(i, weight=1)


bn_up = Button(
  buttons_panel, text="↑", font=("arial", 10), fg="white", bg="black", command=f_up
)
bn_down = Button(
  buttons_panel, text="↓", font=("arial", 10), fg="white", bg="black", command=f_down
)
bn_left = Button(
  buttons_panel, text="←", font=("arial", 10), fg="white", bg="black", command=f_left
)
bn_right = Button(
  buttons_panel, text="→", font=("arial", 10), fg="white", bg="black", command=f_right
)

# endregion buttons

# region option panel
option_panel = Frame(area_frame, bg="black")
for i in range(4):
  option_panel.columnconfigure(i, weight=1)
for i in range(9):
  option_panel.rowconfigure(i, weight=1)

difficulty_panel_option = Frame(option_panel, bg="red")
difficulty_panel_option.rowconfigure(0, weight=1)
for i in range(5):
  difficulty_panel_option.columnconfigure(i, weight=1)
# endregion option panel

# region result panel
result_panel = Frame(area_frame, bg="black")
for i in range(4):
  difficulty_panel_option.columnconfigure(i, weight=1)
for i in range(4):
  difficulty_panel_option.rowconfigure(i, weight=1)


result_message = Label(
  result_panel,
  text="GAME OVER!",
  font=("times new roman", 15, "bold"),
  fg="red",
  bg="black",
)

score_result = Label(
  result_panel,
  text=f"Score: {score}",
  font=("times new roman", 10, "bold"),
  fg="white",
  bg="black",
)

# endregion result panel

# endregion FRAMES

# region MESSAGES

difficulty_option = Label(
  difficulty_panel_option,
  text=difficulty,
  font=("times new roman", 15),
  fg="black",
  bg="white",
)

# endregion MESSAGES

# region BUTONS

bn_options = Button(
  top_panel, text=":", font=("arial", 15), fg="white", bg="black", command=f_option
)


bn_resume = Button(
  option_panel,
  text="RESUME",
  font=("times new roman", 15),
  fg="black",
  bg="white",
  command=f_resume,
)
bn_reset = Button(
  option_panel,
  text="RESET",
  font=("times new roman", 15),
  fg="black",
  bg="white",
  command=f_reset,
)
bn_quit = Button(
  option_panel,
  text="QUIT",
  font=("times new roman", 15),
  fg="black",
  bg="white",
  command=window.destroy,
)

bn_bk = Button(
  difficulty_panel_option,
  text="<",
  font=("arial", 15),
  fg="black",
  bg="white",
  command=f_bk,
)
bn_fd = Button(
  difficulty_panel_option,
  text=">",
  font=("arial", 15),
  fg="black",
  bg="white",
  command=f_fd,
)

bn_reset_o = Button(
  result_panel,
  text="RESET",
  font=("times new roman", 15),
  fg="black",
  bg="white",
  command=f_reset,
)
bn_quit_o = Button(
  result_panel,
  text="QUIT",
  font=("times new roman", 15),
  fg="black",
  bg="white",
  command=window.destroy,
)

# endregion BUTONS

# region KEY BINDINGS
window.bind("<Return>", f_play)
window.bind("<space>", f_option)
window.bind("w", f_up)
window.bind("<Up>", f_up)
window.bind("s", f_down)
window.bind("<Down>", f_down)
window.bind("a", f_left)
window.bind("<Left>", f_left)
window.bind("d", f_right)
window.bind("<Right>", f_right)


# ================PLACEMENT===============
# Messages
score_display.grid(column=0, row=0, columnspan=3, sticky=NSEW)

difficulty_option.grid(column=1, row=0, sticky=NSEW)

result_message.grid(column=0, row=0, columnspan=4, rowspan=2, sticky=NSEW)

score_result.grid(column=1, row=2, columnspan=2, sticky=NSEW)

# Buttons
bn_difficulty.grid(column=0, row=0, sticky=NSEW)

bn_easy.grid(column=0, row=0, sticky=NSEW)
bn_medium.grid(column=0, row=1, sticky=NSEW)
bn_hard.grid(column=0, row=2, sticky=NSEW)

bn_play.pack(side="bottom", expand=True)

bn_options.grid(column=3, row=0, sticky=NSEW)

bn_resume.grid(column=1, row=1, columnspan=2, sticky=NSEW)
bn_reset.grid(column=1, row=3, columnspan=2, sticky=NSEW)
bn_quit.grid(column=1, row=7, columnspan=2, sticky=NSEW)

bn_bk.grid(column=0, row=0, sticky=NSEW)
bn_fd.grid(column=2, row=0, sticky=NSEW)

bn_reset_o.grid(column=0, row=3, columnspan=2, sticky=NSEW, padx=20, pady=20)
bn_quit_o.grid(column=2, row=3, columnspan=2, sticky=NSEW, padx=20, pady=20)

bn_up.grid(column=1, row=0, sticky=NSEW)
bn_down.grid(column=1, row=2, sticky=NSEW)
bn_left.grid(column=0, row=1, sticky=NSEW)
bn_right.grid(column=2, row=1, sticky=NSEW)

# Frames
start_panel.pack(fill="x")
top_panel.grid(column=0, row=0, sticky=NSEW)
area_frame.grid(column=0, row=1, sticky=NSEW)
difficulty_panel_option.grid(column=1, row=5, columnspan=2, sticky=NSEW)
buttons_panel.grid(column=0, row=2, sticky=NSEW)


window.mainloop()
