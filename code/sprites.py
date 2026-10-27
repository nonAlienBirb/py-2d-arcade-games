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
        # self.boolets = [Laser() for _ in range(10)]
        # self.boolet_count = 0
        # self.current_boolet =self.boolets[self.boolet_count]

    # def shoot(self, dt):
    #     if is_key_pressed(KEY_SPACE):
    #         self.current_boolet.set_pos(Vector2(self.pos.x, self.pos.y))
    #         self.current_boolet.set_active()

    #         self.current_boolet.shoot_sound()

    #         self.boolet_count = (self.boolet_count + 1) % len(self.boolets)
    #         self.current_boolet = self.boolets[self.boolet_count]

    #     for boolet in self.boolets:
    #         if boolet.is_active:
    #             boolet.update(dt)


    def update(self, dt):
        self.direction.x = int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT))
        self.direction.y = int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))
        self.direction = Vector2Normalize(self.direction)
        
        super().update(dt)
        # self.shoot(dt)

    def draw(self):
        super().draw()
        # for boolet in self.boolets:
        #     if boolet.is_active:
        #         boolet.draw()


class Laser(Sprite):
    def __init__(self, texture):
        super().__init__(texture, Vector2(), LASER_SPEED, Vector2(0, -1))
        self.is_active = False

    def set_active(self):
        self.is_active = True

    def set_pos(self, pos):
        self.pos.x = pos.x
        self.pos.y = pos.y

    def shoot_sound(self):
        play_sound(self.sound)

class Meteor(Sprite):
    def __init__(self, texture, pos, speed):
        super().__init__(texture, pos, speed, Vector2(uniform(-0.5,0.5),1)) 
        self.exploded = False
        self.rePos_timer = Timer(0.4, False, False, self.reset_Pos)
        self.timer_is_active = False

    def update(self, dt):
        super().update(dt)
        if self.pos.y > WINDOW_HEIGHT:
            if not self.timer_is_active:
                self.rePos_timer.activate()
                self.timer_is_active = True
            self.rePos_timer.update()

    # def reset_Pos(self):
    #     self.pos = Vector2(uniform(0, WINDOW_WIDTH - METEOR_WIDTH ) , ( 0 - METEOR_HEIGHT)/2)
    #     self.rePos_timer.deactivate()
    #     self.timer_is_active = False

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

