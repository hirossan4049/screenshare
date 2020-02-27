# install_twisted_rector must be called before importing and using the reactor
import zlib

import cv2
import numpy
from PIL import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.context_instructions import Rotate
from kivy.graphics.texture import Texture
from kivy.graphics.vertex_instructions import Rectangle
from kivy.support import install_twisted_reactor
from kivy.logger import Logger

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol
from mss import mss
import time


# from timeout_decorator import timeout, TimeoutError

class EchoServer(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)


class EchoServerFactory(protocol.Factory):
    protocol = EchoServer

    def __init__(self, app):
        self.app = app


# @timeout(0.5)
# def inputdata(data):
#     global currentMouseX, currentMouseY


WIDTH = 1920
HEIGHT = 1080
from kivy.app import App
from kivy.uix.label import Label


class TwistedServerApp(App):
    label = None

    def build(self):
        self.label = Label(text="server started\n")
        reactor.listenTCP(8000, EchoServerFactory(self))
        self.texture = Texture.create(size=(WIDTH, HEIGHT))
        self.cashe_img = None
        self.bytes = bytes()
        return self.label

    def handle_message(self, msg):
        if len(msg) == 65536:
            self.bytes += msg
            Logger.info("65536bytes skip")
        else:
            Logger.debug("======START=======")
            self.bytes += msg
            # try:
            decompress_data = zlib.decompress(self.bytes)
            print("new_image", len(decompress_data))
            decompress_data = Image.frombytes("RGB", (1920, 1080), decompress_data).transpose(Image.FLIP_TOP_BOTTOM)
            # decompress_data = self.bytes
            # decompress_data = numpy.fromstring(self.bytes, dtype='uint8')
            # pil_img = Image.fromarray(decompress_data)  #変更点2

            # decompress_data = cv2.imdecode(numpy.frombuffer(decompress_data, dtype=numpy.uint8), cv2.IMREAD_COLOR)

            # try:
            # FIXME: data

            # result = numpy.where(mask == 255, foreground, roi)
            # dst = self.cashe_img + decompress_data
            # dst = cv2.bitwise_and(self.cashe_img,decompress_data)
            # self.cashe_img = dst

            self.texture.blit_buffer(decompress_data.tobytes(), colorfmt='bgr')
            # self.texture.blit_buffer(decompress_data.tobytes())
            # self.texture.flip_vertical()
            with self.root.canvas:
                # self.root.rect.self.texture = self.texture
                self.root.rect = Rectangle(texture=self.texture, pos=(0, 0), size=Window.size)

            # except:
            #     Logger.error("dst or texure error.")
                # self.cashe_img = decompress_data
            # self.texture.blit_buffer(dst.tostring(),colorfmt='bgr')
            # # self.texture.flip_vertical()
            # with self.root.canvas:
            #     # self.root.rect.self.texture = self.texture
            #     self.root.rect = Rectangle(texture=self.texture, pos=(0, 0), size=Window.size)

            self.bytes = bytes()
            # except:
            #     print("失敗")
            # finally:
            #     self.bytes = bytes()

        # except:
        #     self.label.text += "ERROR: {}\n".format("ERROR")
        #     print("ERROR")


if __name__ == '__main__':
    TwistedServerApp().run()
