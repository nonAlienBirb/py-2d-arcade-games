from settings import *
from custom_timer import Timer
from sprites import Player, Laser, Meteor, Explosion

class Game:
    def __init__(self):
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, 'SpriteGame')
        init_audio_device()
        self.import_assets()
        self.player = Player(self.assets['player'])

    def import_assets(self):
        self.IMAGES = Path(__file__).parent.parent / "images"
        self.AUDIOS = Path(__file__).parent.parent / "audio"

        self.assets = {
             'player' : load_texture(str(self.IMAGES / 'spaceship.png')),
             'laser' : load_texture(str(self.IMAGES / 'laser.png')),
             'meteor' : load_texture(str(self.IMAGES / 'meteor.png')),
             'explosion' : [load_texture(str(self.IMAGES / 'explosion' / f'{i}.png')) for i in range(1,29)]
        }

        self.audios = {
             'laser-sound' : str(self.AUDIOS / 'laser.wav')
        }
    def update(self):
            dt = get_frame_time()
            self.player.update(dt)

    def draw(self):
            begin_drawing()
            clear_background(BG_COLOR)
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