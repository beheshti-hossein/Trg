# -*- coding: utf-8 -*-
"""
Colorful animated heart drawn with turtle.
Uses only the Python standard library (turtle, math, colorsys).
"""

import math
import colorsys
import turtle

# --- Settings ---
SCALE = 18           # Size of the outer heart
LAYERS = 22          # Number of nested filled hearts
STEPS = 360          # Points per heart outline (higher = smoother)
POINTS_PER_FRAME = 12  # Points drawn per screen update (higher = faster)
TEXT = "I Love Python"


def heart_point(t, scale):
    """Parametric heart equation, returns (x, y) for angle t."""
    x = 16 * math.sin(t) ** 3
    y = (13 * math.cos(t) - 5 * math.cos(2 * t)
         - 2 * math.cos(3 * t) - math.cos(4 * t))
    return x * scale, y * scale + scale * 2  # small upward shift to center


def gradient_color(ratio):
    """Red -> pink -> purple gradient. ratio is in [0, 1]."""
    hue = (0.0 - 0.22 * ratio) % 1.0     # 0.0 = red, going back toward purple
    sat = 0.95 - 0.25 * ratio
    val = 1.0 - 0.1 * ratio
    return colorsys.hsv_to_rgb(hue, sat, val)


def rainbow_color(ratio):
    """Full rainbow color for the glowing outline."""
    return colorsys.hsv_to_rgb(ratio % 1.0, 1.0, 1.0)


def setup_screen():
    """Create a black window and disable automatic redraw for speed."""
    screen = turtle.Screen()
    screen.title("Colorful Heart")
    screen.bgcolor("black")
    screen.setup(width=800, height=750)
    screen.colormode(1.0)
    screen.tracer(0)
    return screen


def draw_outline(pen, screen, scale):
    """Animate the outer heart outline with rainbow colors."""
    pen.pensize(4)
    pen.penup()
    pen.goto(heart_point(0, scale))
    pen.pendown()
    for i in range(STEPS + 1):
        t = 2 * math.pi * i / STEPS
        pen.pencolor(rainbow_color(i / STEPS))
        pen.goto(heart_point(t, scale))
        if i % POINTS_PER_FRAME == 0:
            screen.update()
    screen.update()


def draw_filled_heart(pen, scale, color):
    """Draw one filled heart of the given size and color."""
    pen.penup()
    pen.goto(heart_point(0, scale))
    pen.color(color)
    pen.begin_fill()
    for i in range(STEPS + 1):
        pen.goto(heart_point(2 * math.pi * i / STEPS, scale))
    pen.end_fill()


def draw_layers(pen, screen):
    """Fill the heart layer by layer, from outside to inside."""
    for layer in range(LAYERS):
        ratio = layer / (LAYERS - 1)
        scale = SCALE * (1 - ratio * 0.92)  # shrink toward the center
        draw_filled_heart(pen, scale, gradient_color(ratio))
        screen.update()
        screen.getcanvas().after(35)  # short pause between layers


def write_text(pen, screen):
    """Write the message below the heart."""
    pen.penup()
    pen.goto(0, -SCALE * 19)
    pen.color("white")
    pen.write(TEXT, align="center", font=("Arial", 28, "bold"))
    screen.update()


def main():
    screen = setup_screen()
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)

    draw_outline(pen, screen, SCALE)   # 1) animated rainbow outline
    draw_layers(pen, screen)           # 2) nested gradient fill
    draw_outline(pen, screen, SCALE)   # 3) redraw outline on top
    write_text(pen, screen)            # 4) message

    turtle.done()  # keep the window open until the user closes it


if __name__ == "__main__":
    main()
