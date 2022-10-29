import turtle
import winsound

playingGame: bool = True

gamePause: bool = True

gameWindow = turtle.Screen()
gameWindow.title("Ping Pong")
gameWindow.setup(800, 700)
gameWindow.bgcolor("green")
gameWindow.tracer(0)

# net
net = turtle.Turtle()
net.speed(0)
net.color("white")
net.width(5)
net.hideturtle()
net.penup()
net.setposition(0, 380)
net.pendown()
net.setposition(0, -380)
net.penup()
net.setposition(400, 270)
net.pendown()
net.setposition(-400, 270)
net.penup()
net.setposition(400, -270)
net.pendown()
net.setposition(-400, -270)
# bat 1

bat_1 = turtle.Turtle()
bat_1.speed(0)
bat_1.shape("square")
bat_1.shapesize(stretch_wid=5, stretch_len=1)
bat_1.color("white")
bat_1.penup()
bat_1.goto(-350, 0)

# bat 1

bat_2 = turtle.Turtle()
bat_2.speed(0)
bat_2.shape("square")
bat_2.shapesize(stretch_wid=5, stretch_len=1)
bat_2.color("white")
bat_2.penup()
bat_2.goto(350, 0)

# ball

ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("black")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.1
ball.dy = -0.1

# score pen
Score_1 = 0
Score_2 = 0
pen = turtle.Turtle()
pen.speed()
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 280)
pen.write(f"Player A: {Score_1} | Player B: {Score_2}", align="center", font=("Courier", 24, "normal"))

# pause
pausePen = turtle.Turtle()
pausePen.speed()
pausePen.color("white")
pausePen.penup()
pausePen.hideturtle()
pausePen.goto(0, 0)


# movements

def bat_1_up():
    y = bat_1.ycor()
    if y >= 280:
        y = 280
    else:
        y += 20
    bat_1.sety(y)


def bat_1_down():
    y = bat_1.ycor()
    if y <= -280:
        y = -280
    else:
        y -= 20
    bat_1.sety(y)


def bat_2_up():
    y = bat_2.ycor()
    if y >= 280:
        y = 280
    else:
        y += 0.08
    bat_2.sety(y)


def bat_2_down():
    y = bat_2.ycor()
    if y <= -280:
        y = -280
    else:
        y -= 0.08
    bat_2.sety(y)


def pause():
    global gamePause
    if gamePause:
        gamePause = False
    else:
        gamePause = True


def bat_2_ai():
    if bat_2.ycor() < ball.ycor():
        bat_2_up()
    elif bat_2.ycor() > ball.ycor():
        bat_2_down()


# keyboard binding

gameWindow.listen()
gameWindow.onkeypress(bat_1_up, "w")
gameWindow.onkeypress(bat_1_down, "s")
gameWindow.onkeypress(pause, "space")

while playingGame:
    try:
        if gamePause:
            pausePen.write(f"| |", align="center", font=("Courier", 64, "bold"))
        else:
            pausePen.clear()
            gameWindow.update()

            # Move Ball
            ball.setx(ball.xcor() + ball.dx)
            ball.sety(ball.ycor() + ball.dy)

            # Border check
            if ball.ycor() > 270:
                ball.sety(270)
                ball.dy = -ball.dy
                winsound.PlaySound("ball.wav", winsound.SND_ASYNC)
            if ball.ycor() < -270:
                ball.sety(-270)
                ball.dy = -ball.dy
                winsound.PlaySound("ball.wav", winsound.SND_ASYNC)

            if ball.xcor() > 390:
                ball.goto(0, 0)
                ball.dx = -ball.dx
                Score_1 += 1
                pen.clear()
                pen.write(f"Player A: {Score_1} | Player B: {Score_2}", align="center", font=("Courier", 24, "normal"))
                winsound.PlaySound("crowd.wav", winsound.SND_ASYNC)

            if ball.xcor() < -390:
                ball.goto(0, 0)
                ball.dx = -ball.dx
                Score_2 += 1
                pen.clear()
                pen.write(f"Player A: {Score_1} | Player B: {Score_2}", align="center", font=("Courier", 24, "normal"))
                winsound.PlaySound("crowd.wav", winsound.SND_ASYNC)

            # collision
            if 340 < ball.xcor() < 350 and bat_2.ycor() + 50 > ball.ycor() > bat_2.ycor() - 50:
                ball.setx(340)
                ball.dx *= -1
                winsound.PlaySound("ball.wav", winsound.SND_ASYNC)
            if -340 > ball.xcor() > -350 and bat_1.ycor() + 50 > ball.ycor() > bat_1.ycor() - 50:
                ball.setx(-340)
                ball.dx *= -1
                winsound.PlaySound("ball.wav", winsound.SND_ASYNC)
            bat_2_ai()
    except Exception:
        break

gameWindow.mainloop()
