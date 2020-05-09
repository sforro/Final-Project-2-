import turtle
import random
import os
import platform

# moved the game inside this function
def game():

    # create the main window
    global wn
    score = 0
    lives = 3

    wn.clear()

    # create the main window
    wn = turtle.Screen()
    wn.title("Cloudy with a Chance of Burgers!")
    wn.bgcolor("green")
    wn.bgpic("skyback.gif")
    wn.setup(width=800, height=600)
    wn.tracer(0)

    wn.register_shape("simp.gif")
    wn.register_shape("burger.gif")
    wn.register_shape("salad.gif")
    wn.register_shape("simpr.gif")
    wn.register_shape("heart.gif")

    # add player
    # starting position (bottom and without drawing line)
    player = turtle.Turtle()
    player.speed(0)
    player.shape("simp.gif")
    player.color("white")
    player.penup()
    player.goto(0, -250)
    player.direction = "stop"

    # list of burgers
    burgers = []

    # add burgers
    for i in range(8):
        burger = turtle.Turtle()
        burger.speed(0)
        burger.shape("burger.gif")
        burger.color("blue")
        burger.penup()
        burger.goto(-100, 250)
        burger.speed = random.randint(1, 2)
        burgers.append(burger)

    # list of salads
    salads = []

    # add salads
    for i in range(12):
        salad = turtle.Turtle()
        salad.speed(0)
        salad.shape("salad.gif")
        salad.color("red")
        salad.penup()
        salad.goto(100, 250)
        salad.speed = random.randint(1, 2)
        salads.append(salad)

    # list of extra lives
    extralives = []

    # add extra lives
    for i in range(1):
        extralive = turtle.Turtle()
        extralive.speed(0)
        extralive.shape("heart.gif")
        extralive.color("red")
        extralive.penup()
        extralive.goto(100, 250)
        extralive.speed = random.randint(1, 2)
        extralives.append(extralive)

    # create the pen to show score and lives
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("black")
    pen.penup()
    pen.goto(0, 250)
    font = ("Helvetica", 25, "normal")
    pen.clear()
    pen.write("Score: {}   Lives: {}".format(score, lives), align="center", font=font)

    # functions
    def go_left():
        player.direction = "left"
        player.shape("simp.gif")

    def go_right():
        player.direction = "right"
        player.shape("simpr.gif")

    # keyboard binding (listening to keyboard)
    wn.listen()
    wn.onkeypress(go_left, "Left")
    wn.onkeypress(go_right, "Right")

    def play_sound(sound_file, time=0):
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
            turtle.ontimer(lambda: play_sound(sound_file, time), t=int(time*1000))

    def kill_sound():
        if platform.system() == "Windows":
            winsound.Playsound(None, windsound.SND_FILENAME)

        elif platform.system() == "Linux":
            os.system("killall aplay")

        else:
            os.system("killall afplay")


    # play bg music
    play_sound("africa.wav", 292)

    # main game loop
    while True:

        # update screen

        wn.update()
        wn.delay(100)

        # player movement
        if player.direction == "left":
            x = player.xcor()
            x -= 3
            player.setx(x)

        if player.direction == "right":
            x = player.xcor()
            x += 3
            player.setx(x)

        # keep player on screen
        if player.xcor() > 380:
            player.setx(380)

        if player.xcor() < -380:
            player.setx(-380)

        # moving burgers
        for burger in burgers:
            y = burger.ycor()
            y -= burger.speed
            burger.sety(y)

            # check for off-screen
            if y < -300:
                # random position after off-screen
                x = random.randint(-380, 380)
                y = random.randint(300, 400)
                burger.goto(x, y)

            # check for collision
            if burger.distance(player) < 40:
                play_sound("coin.wav")
                # random position after collision
                x = random.randint(-380, 380)
                y = random.randint(300, 400)
                burger.goto(x, y)
                score += 10
                pen.clear()
                pen.write("Score: {} Lives: {}".format(score, lives), align="center", font=font)

        # moving salads
        for salad in salads:
            y = salad.ycor()
            y -= salad.speed
            salad.sety(y)

            # check for off-screen
            if y < -300:
                # random position after off-screen
                x = random.randint(-380, 380)
                y = random.randint(300, 400)
                salad.goto(x, y)

            # check for collision
            if salad.distance(player) < 40:
                play_sound("fail.wav")
                # random position after collision
                x = random.randint(-380, 380)
                y = random.randint(300, 400)
                salad.goto(x, y)
                lives -= 1
                pen.clear()
                pen.write("Score: {} Lives: {}".format(score, lives), align="center", font=font)

        for extralive in extralives:
            y = extralive.ycor()
            y -= extralive.speed
            extralive.sety(y)

            # check for off-screen
            if y < -300:
                # random position after off-screen
                x = random.randint(-380, 380)
                y = random.randint(1000, 2000)
                extralive.goto(x, y)

            # check for collision
            if extralive.distance(player) < 40:
                play_sound("life.wav")
                # random position after collision
                x = random.randint(-380, 380)
                y = random.randint(1000, 2000)
                extralive.goto(x, y)
                lives += 1
                pen.clear()
                pen.write("Score: {} Lives: {}".format(score, lives), align="center", font=font)

        # game over screen
        if lives <= 0:
            kill_sound()
            play_sound("over.wav")
            pen.clear()
            pen.goto(0, 0)
            font2 = ("Helvetica", 50, "bold")
            pen.write("GAME OVER!", align="center", font=font2)
            pen.goto(0, -40)
            pen.write("Score: {}".format(score), align="center", font=font)
            pen.goto(0, -80)
            font3 = ("Helvetica", 10, "normal")
            pen.write("Click to quit game.", align="center", font=font3)
            wn.exitonclick()




menu_items = ["Play Game", "Help", "Quit"]
pos_selected = 0 # what is the item selected

def go_menu_up():
    global pos_selected
    pos_selected = (pos_selected - 1 ) % len(menu_items)

def go_menu_down():
    global pos_selected
    pos_selected = (pos_selected + 1 ) % len(menu_items)

# this is where you identify what has been pressed
def go_menu_select():
    global pos_selected

    if pos_selected == 0 :
        # new game
        game()
    elif pos_selected == 1:
        wn.clear()
        wn.title("Cloudy with a Chance of Burgers!")
        wn.bgpic("cloudy.gif")
        wn.setup(width=800, height=600)
        wn.tracer(0)
        pen = turtle.Turtle()
        pen.hideturtle()
        pen.speed(0)
        pen.shape("square")
        pen.color("black")
        pen.penup()
        pen.goto(0, 0)
        font = ("Helvetica", 20, "normal")
        font2 = ("Helvetica", 30, "bold")
        pen.clear()
        pen.write("Instructions", align="center", font=font2)
        pen.goto(0,-50)
        pen.write("Eat hamburgers and avoid salads.", align="center", font=font)
        pen.goto(0,-100)
        pen.write("Catch hearts to get extra lives.", align="center", font=font)
        wn.exitonclick()


    elif pos_selected == 2:
        # in my case exit
        turtle.Screen().bye()

# this is the menu, I have used the heat icon you have :)
def show_menu():

    wn.title("Cloudy with a Chance of Burgers!")
    wn.bgpic("cloudy.gif")
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.shape("square")
    pen.color("black")
    pen.penup()
    pen.goto(0, 0)
    font = ("Arial", 30, "bold")
    pen.clear()

    for i in range(len(menu_items)):
        text = menu_items[i]
        pen.goto(0, 20 - i * 100)
        pen.write(text, align="center", font=font)



score = 0
lives=3

# show the menu
wn = turtle.Screen()
show_menu()

wn.onkeypress(go_menu_up, "Up")
wn.onkeypress(go_menu_down, "Down")
wn.onkeypress(go_menu_select, "Return")
wn.listen()
wn.tracer(0)

wn.register_shape("simp.gif")
wn.register_shape("burger.gif")
wn.register_shape("salad.gif")
wn.register_shape("simpr.gif")
wn.register_shape("cloudy.gif")
wn.register_shape("heart.gif")

# this is the heart to go through the menu
select = turtle.Turtle()
select.speed(0)
select.shape("burger.gif")
select.color('red')
select.penup()
select.goto(-50, 200)



while True:
    wn.update()
    wn.delay(30)
    select.goto(-150, 40 - pos_selected * 100)