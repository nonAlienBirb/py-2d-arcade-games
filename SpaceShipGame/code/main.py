from settings import *
from custom_timer import Timer
from sprites import Player, Laser, Meteor, Explosion

class Game:
    def __init__(self):
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, 'SpriteGame')
        init_audio_device()
        self.import_assets()
        self.lasers, self.meteors = [], []
        self.meteor_creation_timer = Timer(METEOR_TIMER_DURATION, True, True, self.create_meteor)
        self.player = Player(self.assets['player'], self.create_laser)

    def import_assets(self):
        self.IMAGES = Path(__file__).parent.parent / "images"
        self.AUDIOS = Path(__file__).parent.parent / "audio"

        self.assets = {
             'star' : load_texture(str(self.IMAGES / 'star.png')),
             'player' : load_texture(str(self.IMAGES / 'spaceship.png')),
             'laser' : load_texture(str(self.IMAGES / 'laser.png')),
             'meteor' : load_texture(str(self.IMAGES / 'meteor.png')),
             'explosion' : [load_texture(str(self.IMAGES / 'explosion' / f'{i}.png')) for i in range(1,29)]
        }

        self.audios = {
             'laser' : load_sound(str(self.AUDIOS / 'laser.wav')),
             'explosion' : load_sound(str(self.AUDIOS / 'explosion.wav')),
             'background-music' : str(self.AUDIOS / 'music.wav')
        }

        self. star_data = [
             (Vector2(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)), #pos
             uniform(0.5, 1.6) # size
             ) for _ in range(30)
        ]

    def draw_stars(self):
         for star in self.star_data:
            draw_texture_ex(self.assets['star'], star[0], 0, star[1], WHITE)

    def create_laser(self, pos):
         self.lasers.append(Laser(self.assets['laser'], pos))
         play_sound(self.audios['laser'])

    def create_meteor(self):
         self.meteors.append(Meteor(self.assets['meteor']))
    def discard_sprites(self):
         self.lasers = [laser for laser in self.lasers if not laser.discard]
         self.meteors = [meteor for meteor in self.meteors if not meteor.discard]

    def update(self):
            print(len(self.meteors))
            self.discard_sprites()
            dt = get_frame_time()
            self.player.update(dt)
            self.meteor_creation_timer.update()
            for sprite in self.lasers + self.meteors:
                 sprite.update(dt)

    def draw(self):
            begin_drawing()
            clear_background(BG_COLOR)
            self.draw_stars()
            for sprite in self.lasers + self.meteors:
                 sprite.draw()
            self.player.draw()
            end_drawing()
         
    def run(self):
        while not window_should_close():
            self.update()    
            self.draw()
        close_audio_device()
        close_window()  

if __name__ == '__main__':
    game = Game()
    game.run()