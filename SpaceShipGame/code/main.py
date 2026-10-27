from settings import *
from custom_timer import Timer
from sprites import Player, Laser, Meteor, Explosion

class Game:
    def __init__(self):
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, 'SpriteGame')
        init_audio_device()
        self.import_assets()
        play_music_stream(self.audios['music'])
        self.paused = False
        self.lasers, self.meteors, self.explosions = [], [], []
        self.meteor_creation_timer = Timer(METEOR_TIMER_DURATION, True, True, self.create_meteor)
        self.player = Player(self.assets['player'], self.create_laser)

    def import_assets(self):
        self.IMAGES = Path(__file__).parent.parent / "images"
        self.AUDIOS = Path(__file__).parent.parent / "audio"
        self.Font = Path(__file__).parent.parent/ 'font'
        self.assets = {
             'star' : load_texture(str(self.IMAGES / 'star.png')),
             'player' : load_texture(str(self.IMAGES / 'spaceship.png')),
             'laser' : load_texture(str(self.IMAGES / 'laser.png')),
             'meteor' : load_texture(str(self.IMAGES / 'meteor.png')),
             'explosion' : [load_texture(str(self.IMAGES / 'explosion' / f'{i}.png')) for i in range(1,29)],
             'font' : load_font_ex(str(self.Font / 'Stormfaze.otf'), FONT_SIZE, ffi.NULL, 0)
        }

        self.audios = {
             'laser' : load_sound(str(self.AUDIOS / 'laser.wav')),
             'explosion' : load_sound(str(self.AUDIOS / 'explosion.wav')),
             'music' : load_music_stream(str(self.AUDIOS / 'music.wav'))
        }

        self. star_data = [
             (Vector2(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)), #pos
             uniform(0.5, 1) # size
             ) for _ in range(30)
        ]

    def draw_stars(self):
         for star in self.star_data:
            draw_texture_ex(self.assets['star'], star[0], 0, star[1], WHITE)

    def draw_score(self):
         score = int(get_time())
         text_size = measure_text_ex(self.assets['font'], str(score), FONT_SIZE, 0)

         draw_text_ex(self.assets['font'], str(score), Vector2((WINDOW_WIDTH - text_size.x) / 2, 50), FONT_SIZE, 0, WHITE)
    
    def create_laser(self, pos):
         self.lasers.append(Laser(self.assets['laser'], pos))
         play_sound(self.audios['laser'])

    def create_meteor(self):
         self.meteors.append(Meteor(self.assets['meteor']))
    
    def check_collisions(self):
        # lasers & meteors
        for laser in self.lasers:
            for meteor in self.meteors:
                if check_collision_circle_rec(meteor.get_center(), meteor.collision_radius, laser.get_rectangle()):
                    meteor.discard, laser.discard = True, True
                    self.explosions.append(Explosion(self.assets['explosion'], Vector2(laser.pos.x - laser.size.x / 2  , laser.pos.y)))
                    play_sound(self.audios['explosion'])
        # meteors & player
        for meteor in self.meteors:
            if check_collision_circles(self.player.get_center(), self.player.collision_radius, meteor.get_center(), meteor.collision_radius):
                # self.explosions.append(Explosion(self.assets['explosion'], Vector2()))
                self.pause_game()
                print('GAME OVER')
    
    def discard_sprites(self):
         self.lasers = [laser for laser in self.lasers if not laser.discard]
         self.meteors = [meteor for meteor in self.meteors if not meteor.discard]
         self.explosions = [explosion for explosion in self.explosions if not explosion.discard]

    def pause_game(self):
         self.paused = True

    def update(self):
            self.discard_sprites()
            dt = get_frame_time()
            if not self.paused:
                self.player.update(dt)
                self.meteor_creation_timer.update()
                for sprite in self.lasers + self.meteors + self.explosions:
                    sprite.update(dt)
            self.check_collisions()
            update_music_stream(self.audios['music'])

    def draw(self):
            begin_drawing()
            clear_background(BG_COLOR)
            self.draw_stars()
            self.draw_score()
            for sprite in self.lasers + self.meteors + self.explosions:
                 sprite.draw()
            self.player.draw()
            end_drawing()
         
    def run(self):
        while not window_should_close():
            self.update()    
            self.draw()
        unload_music_stream(self.audios['music'])
        close_audio_device()
        close_window()  

if __name__ == '__main__':
    game = Game()
    game.run()