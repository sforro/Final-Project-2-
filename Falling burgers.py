import turtle
import random
import os
import platform

# if on windows you need to import winsound
if platform.system() == "Windows":
    try:
        import winsound
    except:
        print("Winsound module not available.")

score = 0
lives = 3

wn = turtle.Screen()
wn.title("our game name")
wn.bgcolor("green")
wn.bgpic("skyback.gif")
wn.setup(width=800, height=600)
wn.tracer(0)

wn.register_shape("simp.gif")
wn.register_shape("simpr.gif")
wn.register_shape("burger.gif")
wn.register_shape("salad.gif")

# player
player = turtle.Turtle()
player.speed(0)
player.shape("simpr.gif")
player.color("white")
player.penup()
player.goto(0, -250)
player.direction = "stop"

# list of burgers
burgers = []

# add burgers
for _ in range(20):
    burger = turtle.Turtle()
    burger.speed(0)
    burger.shape("burger.gif")
    burger.color("blue")
    burger.penup()
    burger.goto(0, 250)
    burger.speed = random.randint(1, 4)
    burgers.append(burger)

salads = []

# add salads
for _ in range(20):
    salad = turtle.Turtle()
    salad.speed(0)
    salad.shape("salad.gif")
    salad.color("red")
    salad.penup()
    salad.goto(0, 250)
    salad.speed = random.randint(1, 4)
    salads.append(salad)

# make pen
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.goto(0, 260)
font = ("Courier", 24, "normal")
pen.write("Score {} Lives {}".format(score, lives), align="center", font=font)


# functions
def go_left():
    player.direction = "left"
    player.shape("simp.gif")


def go_right():
    player.direction = "right"
    player.shape("simpr.gif")


def play_sound(sound_file, time = 0):
    # windows
    if platform.system() == "Windows":
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    # linux
    elif platform.system() == "Linux":
        os.system("aplay -q {}&".format(sound_file))
    # mac
    else:
        os.system("afplay {}&".format(sound_file))

    # repeat sound
    if time > 0:
        turtle.ontimer(lambda: play_sound(sound_file, time), t=int(time * 1000))


# keyboard binding (listening to keyboard)
wn.listen()
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# play bg music
play_sound("africa.wav", 294)

# main game loop
while True:

    # update screen
    wn.update()

    # player moving
    if player.direction == "left":
        x = player.xcor()
        x -= 3
        player.setx(x)

    if player.direction == "right":
        x = player.xcor()
        x += 3
        player.setx(x)

    # moving burgers
    for burger in burgers:
        y = burger.ycor()
        y -= burger.speed
        burger.sety(y)

        # check for off-screen
        if y < -300:
            x = random.randint(-380, 380)
            y = random.randint(300, 400)
            burger.goto(x, y)

        # check for collision
        if burger.distance(player) < 40:
            play_sound("coin.wav")
            x = random.randint(-380, 380)
            y = random.randint(300, 400)
            burger.goto(x, y)
            score += 10
            pen.clear()
            pen.write("Score {} Lives {}".format(score, lives), align="center", font=font)

    # moving salads
    for salad in salads:
        y = salad.ycor()
        y -= salad.speed
        salad.sety(y)

        # check for off-screen
        if y < -300:
            x = random.randint(-380, 380)
            y = random.randint(300, 400)
            salad.goto(x, y)

        # check for collision
        if salad.distance(player) < 40:
            play_sound("fail.wav")
            x = random.randint(-380, 380)
            y = random.randint(300, 400)
            salad.goto(x, y)
            score -= 10
            lives -= 1
            pen.clear()
            pen.write("Score {} Lives {}".format(score, lives), align="center", font=font)

wn.mainloop()
