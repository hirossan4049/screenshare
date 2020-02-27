import socket
import time
import zlib

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
HEIGHT = 1200



class EchoClient(protocol.Protocol):
    def connectionMade(self):
        print("connected!")
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        self.factory.app.print_message(data.decode('utf-8'))
#
# class EchoClientSecond(protocol.Protocol):
#     def connectionMade(self):
#         print("connected second!")
#         self.factory.app.on_connection_sec(self.transport)
#
#     def dataReceived(self, data):
#         self.factory.app.print_message(data.decode('utf-8'))
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

# class EchoClientFactorySecond(protocol.ClientFactory):
#     protocol = EchoClientSecond
#     def __init__(self, app):
#         self.app = app
#
#     def startedConnecting(self, connector):
#         print('Started to connect2.')
#
#     def clientConnectionLost(self, connector, reason):
#         print('Lost connection2.')
#
#     def clientConnectionFailed(self, connector, reason):
#         print('Connection failed2.')


class MainWindow(BoxLayout):
    textinput = StringProperty()
    status = StringProperty()
    def __init__(self,**kwargs):
        super(MainWindow,self).__init__(**kwargs)
        self.sct = mss()
        self.rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}
        self.backimg = bytes()
        self.connect_to_server()
        # self.textinput = requests.get("https://google.com").text

    def connect_to_server(self):
        Logger.info("connect_to_server")
        # reactor.connectTCP('127.0.0.1', 8000, EchoClientFactory(self))
        reactor.connectTCP('192.168.11.33', 8000, EchoClientFactory(self))
        # reactor.connectTCP('10.12.100.246', 8000, EchoClientFactorySecond(self))
        # reactor.connectTCP('192.168.11.28', 8000, EchoClientFactory(self))

    def on_connection(self, connection):
        # sendmessage = "conectted"
        self.connection = connection
        # print(sendmessage)
        # self.connection.write(sendmessage.encode())
        # self.update()
        Clock.schedule_interval(self.update, 1)




    def update(self,key, *largs):
        sct_img = self.sct.grab(self.rect)
        image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        image = image.resize((int(image.width / 2), int(image.height / 2)))
        print(image.size)
        if not self.backimg == image:
            self.backimg = image

            print(len(image.tobytes()))
            compress_data = zlib.compress(image.tobytes())
            # self.connection.write(compress_data)
            len_compless = len(compress_data)
            print(len_compless)
            # print("nomalsize",len(image.tobytes()))
            # print("compless",len(compress_data))
            # data_list = []
            # olddata_list = list(compress_data)
            for i in range(len_compless):
                # print(compress_data[:65536])
                # compress_data = compress_data[:65536]
                if i % 65535 == 0:
                    # print(i)
                    # data_list.append(compress_data[:65536])
                    self.connection.write(compress_data[:65536])
                    compress_data = compress_data[65536:]
                    print("range",i)
                    # time.sleep(1)
        else:
            print("同じ。")
        # image = image.resize((int(image.width / 5), int(image.height / 5)),Image.LANCZOS)
        # print(image.size)

                # del olddata_list[:65536]

        # data_list.append((compress_data[::]))
        # datalen = 0
        # for i in data_list:
        #     datalen += len(i)
        #
        # print(datalen)
        # print(len(data_list))
        # # print(len(compress_data))
        # # img_string = str(sct_img.size.width) +","+ str(sct_img.size.height) + "&&" + str(compress_data)
        # # self.connection.write(img_string.encode())
        # for data in data_list:
        #     print(type(data))
        #     self.connection.write(data)





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
