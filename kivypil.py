

from PIL import Image

from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from mss import mss
from kivy.core.window import Window


#===pip3 freeze
# Kivy==1.11.1
# kivymd==0.102.1
#===============


# Builder.load_file("kvfile.kv")
Builder.load_string(
"""
<MainWindow@BoxLayout>
    # canvas:
    #     Rectangle:
    #         size: self.size
    #         pos: self.pos
""")


WIDTH = 1920
HEIGHT = 1080



class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sct = mss()
        self.rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}


    def build(self):
        self.root = Factory.MainWindow()
        print(self.root.children)

        # with mss() as sct:
        #     rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}
        #     sct_img = sct.grab(rect)
        #     image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        #
        # texture = Texture.create(size=image.size)
        # texture.blit_buffer(image.tobytes())
        # texture.flip_vertical()
        # with self.root.canvas.before:
        #     self.root.rect = Rectangle(texture=texture, pos=(0,0), size=Window.size)
        # self.update()
        Clock.schedule_interval(self.update, 0.3)

    def update(self, key, *largs):
        sct_img = self.sct.grab(self.rect)
        image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        texture = Texture.create(size=image.size)
        texture.blit_buffer(image.tobytes())
        texture.flip_vertical()
        with self.root.canvas.before:
            self.root.rect = Rectangle(texture=texture, pos=(0,0), size=Window.size)



if __name__ == "__main__":
    MainApp().run()

