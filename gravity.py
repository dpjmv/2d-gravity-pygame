from rigidbody import RigidBody
from utils import *
import pygame


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        pygame.mixer.quit()

        self.params = {
            "running": True,
            "screen_size": (1000, 600),
            "fps": 60,
            "max_speed": 100, # pixels/second
            "gravitational_constant": 50000.0, # with pixels as distance unit
            "radius_scale": 2.0,
            "bg_color": pygame.Color(0, 0, 0),
            "body_count": 100,
            "bouncy_edge": False,
            "show_velocity_vector": False,
            "show_fps": False,
        }

        self.screen = pygame.display.set_mode(self.params["screen_size"])
        
        self.clock = pygame.time.Clock()
        self.dt = 1.0 / self.params["fps"]

        self.bodies = [RigidBody(self) for x
                       in range(0, self.params["body_count"])]

    def run(self):
        while self.params["running"]:
            self.clock.tick(self.params["fps"])
            
            self.screen.fill(self.params["bg_color"])
            
            self.update()

            pygame.display.update()

        pygame.quit()

    def update(self):
        event_pool = pygame.event.get()
        for event in event_pool:
            if event.type == pygame.QUIT:
                self.params["running"] = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.params["show_fps"] = not self.params["show_fps"]
                if event.key == pygame.K_r:
                    self.bodies = [RigidBody(self) for x
                       in range(0, self.params["body_count"])]
                if event.key == pygame.K_v:
                    current_vel_vec_state = self.params["show_velocity_vector"]
                    self.params["show_velocity_vector"] = not current_vel_vec_state
                if event.key == pygame.K_e:
                    self.params["bouncy_edge"] = not self.params["bouncy_edge"]

        new_bodies = []
        old_bodies = []
        for i in range(0, len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                a = self.bodies[i]
                b = self.bodies[j]

                if RigidBody.collide(a, b):
                    # use center of mass
                    new_x = ((a.pos[0] * a.mass) + (b.pos[0] * b.mass)) / \
                            (a.mass + b.mass)
                    new_y = ((a.pos[1] * a.mass) + (b.pos[1] * b.mass)) / \
                            (a.mass + b.mass)
                    
                    new_mass = a.mass + b.mass
                    p_a = [a.mass * a.vel[0], a.mass * a.vel[1]] # momentum
                    p_b = [b.mass * b.vel[0], b.mass * b.vel[1]]
                    new_p = [p_a[0] + p_b[0], p_a[1] + p_b[1]]
                    new_vel = [new_p[0] / new_mass, new_p[1] / new_mass]
                    new_body = RigidBody(self, new_mass, (new_x, new_y), new_vel)
                    new_bodies.append(new_body)
                    old_bodies += [i, j]

                RigidBody.apply_forces(self, a, b)
            
            if self.params.get("bouncy_edge"):
                self.bodies[i].collides_edge()

        for body in self.bodies:
            body.move()
            body.draw()

        old_bodies = list(dict.fromkeys(old_bodies)) # Remove duplicates
        old_bodies.sort(reverse=True)
        for body_index in old_bodies:
            del self.bodies[body_index] 
            
        self.bodies += new_bodies

        if self.params["show_fps"]:
            green = pygame.Color(0, 255, 0)
            bg_color = self.params["bg_color"]
            draw_fps(self.screen, 0, 0, 16, green, bg_color, self.clock)


if __name__ == "__main__":
    Game().run()