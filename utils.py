from fps import fps
import numpy as np
import pygame


def rndint(n):
    return int(round(n))


def normalize(vector):
    norm = float(np.linalg.norm(vector))
    if norm > 0:
        new_vec = np.array([vector[0] / norm, vector[1] / norm])
        return new_vec
    return np.array((0, 0))


def draw_vector(screen, origin, vector, color=pygame.Color(0, 255, 0)):
    """
    vector is an array or tuple
    """
    line_v = np.array(vector)

    arrow_width = 10
    arrow_height = np.linalg.norm(line_v) - 5

    top = [origin[0] + vector[0], origin[1] + vector[1]]
    u = normalize(line_v)
    arrow_bottom = np.array(origin) + (arrow_height * u)
    
    arrow_v = np.array((-u[1], u[0]))
    arrow_wing1 = arrow_bottom + ((arrow_width / 2) * arrow_v)
    arrow_wing2 = arrow_bottom - ((arrow_width / 2) * arrow_v)

    pygame.draw.aaline(screen, color, origin, top)
    pygame.draw.aaline(screen, color, arrow_wing1, top)
    pygame.draw.aaline(screen, color, arrow_wing2, top)


def draw_fps(screen, x, y, size, color, bg_color, clock):
    framerate = fps.get(clock)
    font = pygame.font.SysFont("Arial", size)

    text = font.render(str(framerate), True, color, bg_color)
    screen.blit(text, (x, y))