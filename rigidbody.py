from math import cos, sin, pi, sqrt
from utils import *
import random
import pygame


class RigidBody:
    def __init__(self, game, mass=None, pos=None, vel=None):
        self.game = game

        self.mass = mass
        if not mass:
            self.mass = 1

        if not pos:
            width = game.params["screen_size"][0]
            height = game.params["screen_size"][1]
            self.pos = [random.uniform(10, width - 10),
                        random.uniform(10, height - 10)]
        else:
            self.pos = [pos[0], pos[1]]

        if not vel:
            speed = random.uniform(0, game.params["max_speed"])
            angle = random.uniform(0, 2 * pi)
            self.vel = [speed * cos(angle), speed * sin(angle)]
        else:
            self.vel = [vel[0], vel[1]]

        self.forces = [0.0, 0.0]

    def radius(self):
        return self.game.params["radius_scale"] * (self.mass ** (1/3))

    @staticmethod
    def apply_forces(game, a, b):
        G = game.params["gravitational_constant"]
        m1 = a.mass
        m2 = b.mass
        dx = b.pos[0] - a.pos[0]
        dy = b.pos[1] - a.pos[1]
        d_squared = dx * dx + dy * dy
        d = d_squared ** 0.5
        
        magnitude = (G * m1 * m2) / d_squared
        dx_normalized_scaled = dx / d * magnitude
        dy_normalized_scaled = dy / d * magnitude

        a.forces[0] += dx_normalized_scaled
        b.forces[0] -= dx_normalized_scaled
        a.forces[1] += dy_normalized_scaled
        b.forces[1] -= dy_normalized_scaled

    @staticmethod
    def collide(a, b):
        dx = b.pos[0] - a.pos[0]
        dy = b.pos[1] - a.pos[1]
        d_squared = dx * dx + dy * dy
        radius_sum = a.radius() + b.radius()

        if d_squared < radius_sum ** 2:
            return True
        return False

    def collides_edge(self, bounce=True):
        pos = self.pos
        x, y = pos
        width, height = self.game.params["screen_size"]
        radius = self.radius()
    
        collides = False
        if x - radius <= 0 or x + radius >= width:
            collides = True
            new_vel = [-self.vel[0], self.vel[1]]
        if y - radius <= 0 or y + radius >= height:
            collides = True
            new_vel = [self.vel[0], -self.vel[1]]

        if bounce and collides:
            self.vel = new_vel

        return collides

    def move(self):
        dt = self.game.dt
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.vel[0] += self.forces[0] * dt / self.mass # acceleration
        self.vel[1] += self.forces[1] * dt / self.mass
        self.forces = [0.0, 0.0]

    def draw(self):
        screen = self.game.screen
        white = pygame.Color(255, 255, 255)

        pos_x = rndint(self.pos[0])
        pos_y = rndint(self.pos[1])
        radius = rndint(self.radius())
        pygame.draw.circle(screen, white,
                           (pos_x, pos_y),
                           radius)
        
        if self.game.params["show_velocity_vector"]:
            draw_vector(self.game.screen, self.pos, self.vel)