import socket
import time
import zlib

import cv2
import numpy as numpy
from PIL import Image
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, protocol
# import threading
# install_twisted_rector must be called before importing the reactor
from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
# from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.logger import Logger
from mss import mss
import requests

# Builder.load_file("layout.kv")
WIDTH = 1920
HEIGHT = 1080



class EchoClient(protocol.Protocol):
    def connectionMade(self):
        print("connected!")
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        self.factory.app.print_message(data.decode('utf-8'))
#

class EchoClientFactory(protocol.ClientFactory):
    protocol = EchoClient
    def __init__(self, app):
        self.app = app

    def startedConnecting(self, connector):
        print('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.')

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed.')



class MainWindow(BoxLayout):
    textinput = StringProperty()
    status = StringProperty()
    def __init__(self,**kwargs):
        super(MainWindow,self).__init__(**kwargs)
        self.sct = mss()
        self.rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}
        self.backimg = bytes()
        self.connect_to_server()

        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        # self.textinput = requests.get("https://google.com").text

    def connect_to_server(self):
        Logger.info("connect_to_server")
        reactor.connectTCP('10.12.100.133', 8000, EchoClientFactory(self))

    def on_connection(self, connection):
        self.connection = connection
        Clock.schedule_interval(self.update, 1)




    def update(self,key, *largs):
        sct_img = numpy.array(self.sct.grab(self.rect))
        image = cv2.resize(sct_img,(1920,1080))
        fgmask = self.fgbg.apply(image)
        # cv2.imwrite("fgmask.png",fgmask)

        dst = cv2.bitwise_or(image, image, mask=fgmask)

        # cv2.imwrite("dst.png",dst)
        # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 25]
        # result, encimg = cv2.imencode('.jpg', dst, encode_param)

        # compress_data = cv2.imencode('.jpg', dst)[1].tobytes()

        # print(len(encimg.tobytes()))
        # compress_data = encimg.tobytes()
        # print(dst.shape[2])
        # # opencv -> PIL IMage
        # new_image = dst.copy()
        # new_image = Image.fromarray(new_image)
        # print("new_image",len(new_image.tobytes()))
        print("size",dst.size)
        compress_data = zlib.compress(dst.tobytes(),5)
        len_compless = len(compress_data)
        print(len_compless)
        for i in range(len_compless):
            if i % 65535 == 0:
                self.connection.write(compress_data[:65536])
                compress_data = compress_data[65536:]





class MainApp(App):
    def __init__(self,**kwargs):
        super(MainApp,self).__init__(**kwargs)

    def build(self):
        self.root = Factory.MainWindow()
        self.title = "screenshare"
    # def onClick(self):
    #     print("clicked")


if __name__ == '__main__':
    MainApp().run()
