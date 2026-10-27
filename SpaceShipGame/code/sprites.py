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
        self.collision_radius = self.size.y / 2 

    def get_center(self):
        return Vector2(
            self.pos.x + self.size.x /2 , 
            self.pos.y + self.size.y /2)

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

    def get_rectangle(self):
        return Rectangle(self.pos.x, self.pos.y, self.size.x, self.size.y)
    
class Meteor(Sprite):
    def __init__(self, texture):
        pos  = Vector2(randint(0, WINDOW_WIDTH), randint(-150, -50))
        speed = randint(*METEOR_SPEED_RANGE)
        direction = Vector2(uniform(-0.5,0.5),1)
        super().__init__(texture, pos, speed, direction)
        self.rotation = 0
        self.rect = Rectangle(0, 0, self.size.x, self.size.y)
    def get_center(self):
        return Vector2(self.pos.x, self.pos.y)
    def update(self, dt):
        super().update(dt)
        self.rotation += 50 * dt

    def draw(self):
        target_rect = Rectangle(self.pos.x, self.pos.y, self.size.x, self.size.y)
        draw_texture_pro(self.texture, self.rect, target_rect, Vector2(self.size.x /2, self.size.y /2), self.rotation, WHITE)

class Explosion:
    def __init__(self, frames, pos):
        self.frames = frames
        self.pos = pos
        self.speed = 30
        self.frame_index = 0
        self.discard = False

    def update(self, dt):
        if self.frame_index < len(self.frames) - 1:
            self.frame_index += self.speed * dt
        else:
            self.discard = True
    def draw(self):
        draw_texture_v(self.frames[int(self.frame_index)], self.pos, WHITE)
        
    def explode(self, dt):
        self.frame_index += self.speed * dt
        draw_texture_v(self.frames[int(self.frame_index % len(self.frames))], self.pos, WHITE)

