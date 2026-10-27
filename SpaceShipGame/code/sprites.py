from settings import *
from custom_timer import Timer

class Sprite:
    def __init__(self, texture, pos: Vector2, speed, direction):
        self.texture = texture
        self.size = Vector2(texture.width, texture.height)
        self.pos = pos
        self.speed = speed
        self.direction = direction

    def update(self, dt):
        self.pos.x += self.speed * self.direction.x * dt
        self.pos.y += self.speed * self.direction.y * dt

    def draw(self):
        draw_texture_v(self.texture, self.pos, WHITE)

class Player(Sprite):
    def __init__(self, texture):
        super().__init__(texture, Vector2(WINDOW_WIDTH /2 , WINDOW_HEIGHT/2) , PLAYER_SPEED, Vector2())

    def get_input(self):
        self.direction.x = int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT))
        self.direction.y = int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))
        self.direction = Vector2Normalize(self.direction)

        if is_key_pressed(KEY_SPACE):
            print('shooting laser')
    def update(self, dt):
        self.get_input()
        super().update(dt)
    def draw(self):
        super().draw()

class Laser(Sprite):
    def __init__(self, texture):
        super().__init__(texture, Vector2(), LASER_SPEED, Vector2(0, -1))

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

