from turtle import Turtle


def tree(tList, length, angle, factor):
    if length > 5:
        lst = []
        for t in tList:
            t.forward(length);
            temp = t.clone();
            t.left(angle);
            temp.right(angle);
            lst.append(t);
            lst.append(temp);
        tree(lst, length * factor, angle, factor);


def makeTree(x, y):
    t = Turtle();
    t.color('green');
    t.pensize(5);
    t.hideturtle();
    # t.getscreen().tracer(30,0);
    t.speed(10);
    t.left(90);
    t.penup();
    t.goto(x, y);
    t.pendown();
    t = tree([t], 110, 65, 0.6375);


makeTree(0, 0)