import math
import random
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import numpy as np
import pygame as pg


WINDOW_SIZE = (800, 600)
FPS = 60

pg.init()
window = pg.display.set_mode(WINDOW_SIZE)
clock = pg.time.Clock()
font = pg.font.SysFont("monospace", 20)


def make_circle_array(diameter, hue):
    circle = np.zeros([diameter, diameter, 3])
    center = (diameter - 1) / 2
    radius = diameter / 2

    color = pg.Color("white")
    color.hsva = hue, 100, 100, 100
    color = color[:3]

    # TODO: This could be vectorized using numpy.hypot()
    # TODO: I only need to do this for a quadrant and then mirror the result around.
    # TODO: Could use 2d array and just put int(color) in there. Test if this is faster.
    for x in range(diameter):
        for y in range(diameter):
            dx = x - center
            dy = y - center
            dist = math.hypot(dx, dy)
            if dist <= radius:
                circle[x, y] = color
    return circle


hues = (0, 120, 240)
angles = [math.radians(i) for i in (0, 120, 240)]
window_center_x = WINDOW_SIZE[0] // 2
window_center_y = WINDOW_SIZE[1] // 2
distance_from_center = 75
circle_surfs = [None, None, None]
circle_rects = [None, None, None]
for i in range(3):
    circle = make_circle_array(200, hues[i])
    circle_surf = pg.surfarray.make_surface(circle)
    circle_surfs[i] = circle_surf
    circle_rect = circle_surf.get_rect()
    circle_rect.center = [
        window_center_x + math.sin(angles[i]) * distance_from_center,
        window_center_y - math.cos(angles[i]) * distance_from_center
    ]
    circle_rects[i] = circle_rect


running = True
while running:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    window.fill(pg.Color("black"))
    fps_text = font.render(f"{clock.get_fps():.0f}", False, pg.Color("white"))
    window.blit(fps_text, (0, 0))

    for i in range(3):
        window.blit(circle_surfs[i], circle_rects[i], special_flags=pg.BLEND_RGB_ADD)

    pg.display.flip()
