import turtle

def main():
    turtle.hideturtle()
    square(100, 0, 50, 'blue')

def square(x, y, width, color):
    turtle.penup()
    turtle.goto(x, y)
    turtle.fillcolor(color)
    turtle.pendown()
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(width)
        turtle.left(90)
    turtle.end_fill()

main()
