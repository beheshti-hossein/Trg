# -*- coding: utf-8 -*-
"""
Colorful animated heart drawn with turtle.
Uses only the Python standard library (turtle, math, colorsys).
"""

import math
import colorsys
import turtle

# --- Settings ---
SCALE = 22             # Size of the heart
Y_OFFSET = 70          # Shift the heart up to leave room for the text
LAYERS = 14            # Number of nested color layers inside the heart
STEPS = 240            # Points on the heart outline (higher = smoother)
POINTS_PER_FRAME = 4   # Points added per frame (higher = faster)
FRAME_DELAY = 8        # Milliseconds between frames (lower = faster)
TEXT = "I Love Python"


def heart_point(t, scale):
    """Parametric heart equation, returns (x, y) for angle t."""
    x = 16 * math.sin(t) ** 3
    y = (13 * math.cos(t) - 5 * math.cos(2 * t)
         - 2 * math.cos(3 * t) - math.cos(4 * t))
    return x * scale, y * scale + Y_OFFSET


def layer_color(ratio):
    """Red -> pink -> purple gradient. ratio is in [0, 1]."""
    hue = (0.0 - 0.22 * ratio) % 1.0     # 0.0 = red, going back toward purple
    sat = 0.95 - 0.25 * ratio
    val = 1.0 - 0.1 * ratio
    return colorsys.hsv_to_rgb(hue, sat, val)


def rainbow_color(ratio):
    """Full rainbow color for the outline."""
    return colorsys.hsv_to_rgb(ratio % 1.0, 1.0, 1.0)


def setup_screen():
    """Create a black window and disable automatic redraw for speed."""
    screen = turtle.Screen()
    screen.title("Colorful Heart")
    screen.bgcolor("black")
    screen.setup(width=950, height=900)
    screen.colormode(1.0)
    screen.tracer(0)
    return screen


def fill_wedge(pen, start, end, scale, color):
    """Fill the slice of a heart between angles index start..end."""
    pen.penup()
    pen.goto(0, Y_OFFSET)              # every slice starts from the center
    pen.color(color)                   # same pen color hides seams
    pen.pendown()
    pen.begin_fill()
    for i in range(start, end + 1):
        pen.goto(heart_point(2 * math.pi * i / STEPS, scale))
    pen.goto(0, Y_OFFSET)
    pen.end_fill()


def draw_heart(screen):
    """Grow the heart from one point, filling layers as the outline advances."""
    filler = turtle.Turtle()
    filler.hideturtle()
    filler.pensize(1)

    outliner = turtle.Turtle()
    outliner.hideturtle()
    outliner.pensize(5)
    outliner.penup()
    outliner.goto(heart_point(0, SCALE))   # the starting point
    outliner.pendown()

    for start in range(0, STEPS, POINTS_PER_FRAME):
        end = min(start + POINTS_PER_FRAME, STEPS)

        # Nested layers: big outer slice first, smaller inner slices on top
        for layer in range(LAYERS):
            ratio = layer / (LAYERS - 1)
            scale = SCALE * (1 - ratio * 0.9)
            fill_wedge(filler, start, end, scale, layer_color(ratio))

        # Advance the rainbow outline over the new slice
        for i in range(start + 1, end + 1):
            outliner.pencolor(rainbow_color(i / STEPS))
            outliner.goto(heart_point(2 * math.pi * i / STEPS, SCALE))

        screen.update()
        screen.getcanvas().after(FRAME_DELAY)


def write_text(screen):
    """Write the message below the heart (not inside it)."""
    writer = turtle.Turtle()
    writer.hideturtle()
    writer.penup()
    writer.goto(0, heart_point(math.pi, SCALE)[1] - 70)  # below the tip
    writer.color("white")
    writer.write(TEXT, align="center", font=("Arial", 28, "bold"))
    screen.update()


def main():
    screen = setup_screen()
    draw_heart(screen)
    write_text(screen)
    turtle.done()  # keep the window open until the user closes it


if __name__ == "__main__":
    main()
