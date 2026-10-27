from settings import *
from custom_timer import Timer

class Sprite:
    def __init__(self, texture, pos: Vector2, speed, direction):
        self.texture = texture
        self.size = Vector2(texture.width, texture.height)
        self.pos = pos
        self.speed = speed
        self.direction = direction
        self.discard = False

    def check_discard(self):
        self.discard = not -300 < self.pos.y < WINDOW_HEIGHT + 300

    def move(self, dt):
        self.pos.x += self.speed * self.direction.x * dt
        self.pos.y += self.speed * self.direction.y * dt

    def update(self, dt):
        self.check_discard()
        self.move(dt)

    def draw(self):
        draw_texture_v(self.texture, self.pos, WHITE)

class Player(Sprite):
    def __init__(self, texture , shoot_laser):
        super().__init__(texture, Vector2(WINDOW_WIDTH /2 , WINDOW_HEIGHT/2) , PLAYER_SPEED, Vector2())
        self.shoot_laser = shoot_laser
    def get_input(self):
        self.direction.x = int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT))
        self.direction.y = int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))
        self.direction = Vector2Normalize(self.direction)

        if is_key_pressed(KEY_SPACE):
            self.shoot_laser(Vector2(self.pos.x + self.size.x/2 - 5 , self.pos.y - 30))

    def constraints(self):
        self.pos.x = max(0, min(self.pos.x, WINDOW_WIDTH - self.size.x))
        self.pos.y = max(0, min(self.pos.y, WINDOW_HEIGHT - self.size.y))

    def update(self, dt):
        self.get_input()
        self.constraints()
        self.move(dt)
        
    def draw(self):
        super().draw()

class Laser(Sprite):
    def __init__(self, texture, pos):
        super().__init__(texture, pos, LASER_SPEED, Vector2(0, -1))

class Meteor(Sprite):
    def __init__(self, texture, pos, speed):
        super().__init__(texture, pos, speed, Vector2(uniform(-0.5,0.5),1)) 
        self.exploded = False

class Explosion:
    def __init__(self, frames, pos):
        self.pos = pos
        self.speed = 15
        self.frame_count = 0
        self.EXPLOSION_FRAMES = frames
    def explode(self, dt):
        self.frame_count += self.speed * dt
        self.frame_count = 1 if self.frame_count == 0 else self.frame_count 
        draw_texture(self.EXPLOSION_FRAMES[int(self.frame_count % len(self.EXPLOSION_FRAMES))], self.pos[0],self.pos[1], WHITE)

