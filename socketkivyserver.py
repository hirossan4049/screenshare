# install_twisted_rector must be called before importing and using the reactor
import zlib
import socket

from PIL import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.graphics.vertex_instructions import Rectangle
from kivy.support import install_twisted_reactor



WIDTH = 1920
HEIGHT = 1080
from kivy.app import App
from kivy.uix.label import Label


class TwistedServerApp(App):
    label = None

    def build(self):
        self.label = Label(text="server started\n")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.texture = Texture.create(size=(WIDTH,HEIGHT))
        self.bytes = bytes()
        return self.label

    def handle_message(self, msg):
        # msg = msg.decode()
        # print(msg)
        # try:
        # print("!")
        # img_msg = msg.split("&&")
        # size_list = img_msg[0].split(",")
        # size = int(size_list[0]),int(size_list[1])
        # print(size)
        # print(len(img_msg[1]))
        # print(len(msg))
        # print(type(msg))
        if len(msg) == 65536:
            self.bytes += msg
            # print("65536!まだまだ")
        else:
            print("65536未満！")
            self.bytes += msg
            try:
                decompress_data = zlib.decompress(self.bytes)
                # print(len(decompress_data))
                # image = Image.frombytes("RGB", (3840,2400), decompress_data, "raw", "BGRX")
                # image = Image.frombytes("RGB",(3840, 2160),decompress_data)
                image = Image.frombytes("RGB",(1920, 1080),decompress_data)

                self.texture.blit_buffer(image.tobytes())
                self.texture.flip_vertical()
                with self.root.canvas.before:
                    # self.root.rect.self.texture = self.texture
                    self.root.rect = Rectangle(texture=self.texture, pos=(0, 0), size=Window.size)
            except:
                print("失敗")
            finally:
                self.bytes = bytes()


if __name__ == '__main__':
    TwistedServerApp().run()
