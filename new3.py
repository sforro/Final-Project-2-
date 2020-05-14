import random
import os
import platform
# import pygame
import turtle

# use pygame to play the main music theme
# pygame.init()
# pygame.mixer.music.load("africa.wav")
# pygame.mixer.music.play(loops=-1)


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
        burger.goto(800, 0)
        burger.speed = random.uniform(1, 1.5)
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
        salad.goto(800, 0)
        salad.speed = random.uniform(1, 1.5)
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
        extralive.goto(800, 0)
        extralive.speed = random.uniform(1, 1.5)
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

    def play_again():
        game()

    # keyboard binding (listening to keyboard)
    wn.listen()
    wn.onkeypress(go_left, "Left")
    wn.onkeypress(go_right, "Right")
    wn.onkeypress(play_again, "Return")

    # main game loop
    while True:
        # update screen
        wn.update()
        wn.delay(100)

        # player movement
        if player.direction == "left":
            x = player.xcor()
            x -= 1.7
            player.setx(x)

        if player.direction == "right":
            x = player.xcor()
            x += 1.7
            player.setx(x)

        # keep player in screen
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
                y = random.randint(1000, 2500)
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
            play_sound("over.wav")
            wn.clear()
            wn.title("Cloudy with a Chance of Burgers!")
            wn.bgpic("skyback.gif")
            wn.listen()
            wn.onkeypress(play_again, "Return")
            pen.clear()
            pen.goto(0, 0)
            font2 = ("Helvetica", 70, "bold")
            pen.write("GAME OVER!", align="center", font=font2)
            pen.goto(0, -60)
            pen.write("Score: {}".format(score), align="center", font=font)
            pen.goto(0, -100)
            font3 = ("Helvetica", 10, "normal")
            pen.write("Click to quit game or press enter to play again.", align="center", font=font3)
            wn.exitonclick()


menu_items = []
pos_selected = 0  # what is the item selected


def play_sound(sound_file, time=0):
    # linux
    if platform.system() == "Linux":
        os.system("aplay -q {}&".format(sound_file))
    # windows
    elif platform.system() == "Windows":
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    # mac
    else:
        os.system("afplay {}&".format(sound_file))


def go_menu_up():
    global pos_selected
    pos_selected = (pos_selected - 1) % len(menu_items)


def go_menu_down():
    global pos_selected
    pos_selected = (pos_selected + 1) % len(menu_items)


# this is where you identify what has been pressed
def go_menu_select():
    global pos_selected

    if len(menu_items) == 1:
        # we are in the help
        show_main_menu()
        return
    if pos_selected == 0:
        game()
    elif pos_selected == 1:
        show_help_menu()
    elif pos_selected == 2:
        show_credits()
    elif pos_selected == 3:
        turtle.Screen().bye()


# this is the Main menu
def show_main_menu():
    global menu_items
    menu_items = ["Play Game", "Help", "Credits", "Quit"]

    pen.clear()
    for i in range(len(menu_items)):
        text = menu_items[i]
        pen.goto(0, 20 - i * 100)
        pen.write(text, align="center", font=font)


# this is the help menu
def show_help_menu():
    global menu_items
    menu_items = ["Back", ]
    wn.listen()
    wn.tracer(0)

    pen.clear()

    for i in range(len(menu_items)):
        text = menu_items[i]
        pen.goto(0, -200 - i * 50)
        font2 = ("Arial", 20, "bold")
        pen.write(text, align="center", font=font2)

    pen.goto(0, 0)

    font = ("Helvetica", 20, "normal")
    font2 = ("Helvetica", 30, "bold")
    # pen.clear()
    pen.write("Instructions", align="center", font=font2)
    pen.goto(0, -50)
    pen.write("Eat hamburgers and avoid salads.", align="center", font=font)
    pen.goto(0, -100)
    pen.write("Catch hearts to get extra lives.", align="center", font=font)
    select.goto(-80, -180)


# credits

def show_credits():
    global menu_items
    menu_items = ["Back", ]
    wn.listen()
    wn.tracer(0)

    pen.clear()

    for i in range(len(menu_items)):
        text = menu_items[i]
        pen.goto(0, -220 - i * 50)
        font2 = ("Arial", 20, "bold")
        pen.write(text, align="center", font=font2)

    pen.goto(0, 0)

    font = ("Helvetica", 20, "normal")
    font2 = ("Helvetica", 30, "bold")
    # pen.clear()
    pen.write("Credits", align="center", font=font2)
    pen.goto(0, -50)
    pen.write("Project Manager: Sandra Forro", align="center", font=font)
    pen.goto(0, -100)
    pen.write("Lead Designer: Manuel Afif", align="center", font=font)
    pen.goto(0, -150)
    pen.write("Project Advisor: Bogdan Ratiu", align="center", font=font)
    select.goto(-80, -200)


# this is the initial setup of the screen, we use the 3 global variables: wn, pen, select
def initial_setup():
    # this part is the initial setup of the window, pen and select token
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
    # wn.register_shape("comics.gif") # had to comment bc i dont have this pic so i get an error

    # play_sound("africa.wav", 294)
    wn.title("Cloudy with a Chance of Burgers!")
    wn.setup(width=800, height=600)
    wn.bgpic("cloudy.gif")  # change this back to comics on yours :)

    pen.hideturtle()
    pen.shape("square")
    pen.color("black")
    pen.penup()
    pen.goto(0, 0)

    # this is the burger to go through the menu
    select.speed(0)
    select.shape("burger.gif")
    select.color('red')
    select.penup()
    select.goto(-50, 200)


# this is where the program starts
score = 0
lives = 3

# you define here the 3 main things: the window, the pen and the select.
wn = turtle.Screen()
pen = turtle.Turtle()
select = turtle.Turtle()
font = ("Arial", 30, "bold")

# call the initial setup of the screen, I have made it into a function
initial_setup()

# show the main menu
show_main_menu()

while True:
    wn.update()
    # in help there is no need to change the burger position
    if len(menu_items) > 1:
        select.goto(-150, 40 - pos_selected * 100)
