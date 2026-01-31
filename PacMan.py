import turtle
import time
from collections import deque

TILE_SIZE = 24
PLAYER_SPEED = 24
ENEMY_SPEED = 0.6
TOTAL_LEVELS = 5

#Screen
wn = turtle.Screen()
wn.title(" Pac-Man Advanced ")
wn.bgcolor("black")
wn.setup(width=700, height=700)
wn.tracer(0)

#Mazes
mazes = [
    [
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XP........X            EX",
        "X.X XXX X.X.XXX X XXX   X",
        "X     X     X     X     X",
        "XXX X XXX X XXX X XXX   X",
        "X........X     X        X",
        "X XXX XXX X XXX XXX X   X",
        "X     X     X     X     X",
        "X.XX  X  XXX X XXX X  XXX",
        "X               ........X",
        "X         X             X",
        "X.X XXX X X XXX X XXX   X",
        "X     X     X     X     X",
        "XXX X XXX X XXX X XXX   X",
        "X        X     X        X",
        "X     X     X     X     X",
        "X.XX  X  XXX X XXX X  XXX",
        "X               ........X",
        "XXXXXXXXXXXXXXXXXXXXXXXXX"
    ],
    [
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XP        X . . .      EX",
        "X.X XXX X X.XXX X XXX   X",
        "X     X     X     X     X",
        "XXX X XXX X XXX X XXX . X",
        "X        X     X      . X",
        "X XXX XXX X XXX XXX X . X",
        "X     X.    X     X   . X",
        "X.XX  X. XXX X XXX X  XXX",
        "X                       X",
        "X                       X",
        "X.X XXXXXXXXXXX X XXX   X",
        "X     X     X     X     X",
        "XXX X XXX X XXX X XXX . X",
        "X        X     X      . X",
        "X XXX XXX X XXX XXX X . X",
        "X     X     X     X   . X",
        "X XX  X  XXX X XXX X  XXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX"
    ],
    [
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XP       XXXXXXXX      EX",
        "X..... XX X XXX X XXX   X",
        "X     X     X     X     X",
        "XXX X XXX   XXX X XXX   X",
        "X        X     X        X",
        "X XXX X.X XXX XXX X     X",
        "X     X.    X     X     X",
        "XXXX  X. XXXXX XXX X  XXX",
        "X              .....    X",
        "X        XXXXXXXX      EX",
        "X..... XX X XXX X XXX   X",
        "X     X     X     X     X",
        "XXX X XXX   XXX X XXX   X",
        "X        X     X        X",
        "X XXX X.X XXX XXX X     X",
        "XXXX  X. XXXXX XXX X  XXX",
        "X              .....    X",
        "XXXXXXXXXXXXXXXXXXXXXXXXX"
    ],
    [
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XP       XXXXXXXX      EX",
        "X..... XX X XXX X XXX   X",
        "X    .X     X     X     X",
        "XXX X.XXX   XXX X XXX   X",
        "X    ... X     X        X",
        "X XXX.X.X XXX XXX X     X",
        "X     X     X     X     X",
        "XXXX .X  XXXXX XXX X. XXX",
        "X    .                 EX",
        "X        XXXXXXXX       X",
        "X..... XX X XXX X XXX   X",
        "X    .X     X     X     X",
        "XXX X.XXX   XXX X XXX   X",
        "X        X     X        X",
        "X XXX.X.X XXX XXX X     X",
        "X    .X.    X     X   E X",
        "XXXX .X. XXXXX XXX X  XXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX"
    ],
    [
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XP       ........X     EX",
        "XXXXXX XX X XXX .XXXX   X",
        "X          X    .X      X",
        "XXX X.XXX       X XXX   X",
        "X    ...     XXX        X",
        "X XXX.X X XXX XXX  X    X",
        "X     X     X      X    X",
        "XXXX .X  XXXXX XXX X  XXX",
        "X  ...                 EX",
        "XP       ........X      X",
        "XXXXXX XX X XXX .XXXX   X",
        "X          X    .X      X",
        "XXX X.XXX       X XXX   X",
        "X            XXX..      X",
        "X XXX X X XXX XXX  X    X",
        "XE    X     X      X   EX",
        "XXXX  X  XXXXX XXX X  XXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX"
    ]
]

#Globals
walls = set()
dots = []
enemies = []
player = None
score = 0
lives = 3
current_level = 0
start_pos = (0, 0)
waiting_for_space = False  # 🔹 جدید

#UI
ui = turtle.Turtle()
ui.hideturtle()
ui.penup()
ui.color("white")
ui.goto(-300, 320)

msg = turtle.Turtle()
msg.hideturtle()
msg.penup()
msg.color("yellow")

def update_ui():
    ui.clear()
    ui.write(f"Lives: {lives}   Score: {score}   Level: {current_level+1}" ,
             font=("Arial", 16, "bold"))

def show_message(text, color="yellow"):
    msg.clear()
    msg.color(color)
    msg.goto(0, -280)
    msg.write(text, align="center", font=("Arial", 26, "bold"))

#Classes
class Wall(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("square")
        self.color("pink")
        self.penup()
        self.goto(x, y)
        walls.add((x, y))

class Dot(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.shapesize(0.3)
        self.penup()
        self.goto(x, y)

class Player(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.penup()
        self.color("yellow")
        self.shape("circle")
        self.mouth = True
        self.direction = "Right"
        self.goto(x, y)

    def animate(self):
        self.shape("circle")
        self.mouth = not self.mouth
        self.setheading({"Right":0,"Up":90,"Left":180,"Down":270}[self.direction])

    def move(self, dx, dy, d):
        global score
        x, y = self.xcor()+dx, self.ycor()+dy
        if (x, y) not in walls:
            self.direction = d
            self.goto(x, y)
            self.animate()
            for dot in dots[:]:
                if self.distance(dot) < 10:
                    dot.hideturtle()
                    dots.remove(dot)
                    score += 10
            update_ui()

class Enemy(turtle.Turtle):
    def __init__(self, x, y, target, color):
        super().__init__()
        self.shape("circle")
        self.color(color)
        self.penup()
        self.goto(x, y)
        self.target = target

    def next_move(self):
        start = (self.xcor(), self.ycor())
        goal = (self.target.xcor(), self.target.ycor())
        q = deque([[start]])
        seen = {start}
        while q:
            path = q.popleft()
            x,y = path[-1]
            if (x,y)==goal and len(path)>1:
                return path[1]
            for dx,dy in [(24,0),(-24,0),(0,24),(0,-24)]:
                nx,ny = x+dx,y+dy
                if (nx,ny) not in walls and (nx,ny) not in seen:
                    seen.add((nx,ny))
                    q.append(path+[(nx,ny)])
        return start

    def move_enemy(self):
        self.goto(self.next_move())

#SPACE Handler
def on_space():
    global waiting_for_space
    waiting_for_space = False

wn.listen()
wn.onkey(on_space, "space")

#Build Maze


def build_maze(maze):
    global player, enemies, dots, walls, start_pos
    for t in turtle.turtles():
        t.hideturtle()
    walls.clear(); dots.clear(); enemies.clear()

    sx, sy = -300, 250
    colors = ["red","cyan","orange","green"]

    for y,row in enumerate(maze):
        for x,c in enumerate(row):
            px, py = sx+x*TILE_SIZE, sy-y*TILE_SIZE
            if c=="X": Wall(px,py)
            elif c=="P":
                player = Player(px,py)
                start_pos=(px,py)
            elif c=="E" and len(enemies)<=current_level:
                enemies.append(Enemy(px,py,player,colors[len(enemies)]))
            elif c==".":
                dots.append(Dot(px,py))

    update_ui()
    wn.onkey(lambda: player.move(0,24,"Up"), "Up")
    wn.onkey(lambda: player.move(0,-24,"Down"), "Down")
    wn.onkey(lambda: player.move(-24,0,"Left"), "Left")
    wn.onkey(lambda: player.move(24,0,"Right"), "Right")
    wn.listen()  # 🔹 مهم

#Game Loop


while current_level < TOTAL_LEVELS:
    build_maze(mazes[current_level])
    last = time.time()

    while True:
        wn.update()
        if time.time()-last > ENEMY_SPEED:
            for e in enemies: e.move_enemy()
            last = time.time()

        for e in enemies:
            if player.distance(e)<15:
                lives -= 1
                update_ui()
                if lives==0:
                    show_message(f"GAME OVER\nFinal Score: {score}", "red")
                    wn.update()
                    time.sleep(3)
                    wn.bye()
                player.goto(start_pos)

        if not dots:
            show_message("LEVEL COMPLETE\nPress SPACE to continue")
            waiting_for_space = True
            while waiting_for_space:
                wn.update()
            msg.clear()
            current_level += 1
            break

#WIN


show_message(f"🎉 YOU WIN 🎉\nFinal Score: {score}", "green")
wn.update()
time.sleep(4)
wn.bye()