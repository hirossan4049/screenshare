from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout

Config.set('graphics', 'fullscreen', 0)

from PIL import Image

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from mss import mss
from kivy.core.window import Window

WIDTH = 1920
HEIGHT = 1080


class MainApp(App):
    def build(self):
        self.title = 'テスト'

        layout = Widget()
        layout.size = Window.size

        # image = Image.open('./monitor-1.png')
        with mss() as sct:
            rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}
            sct_img = sct.grab(rect)
            image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        texture = Texture.create(size=image.size)
        texture.blit_buffer(image.tobytes())
        texture.flip_vertical()
        with layout.canvas.before:
            layout.rect = Rectangle(texture=texture, pos=layout.pos, size=layout.size)

        return layout




if __name__ == '__main__':
    MainApp().run()