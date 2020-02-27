# -*- coding: utf-8 -*-
import zlib

import gevent
from PIL import Image
from gevent import socket
from functools import wraps
import time
from mss import mss
HOST = '127.0.0.1'
PORT = 1234

WIDTH = 1920
HEIGHT = 1080

rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}
sct = mss()


def client():
    print("[time]",time.time())
    conn = socket.create_connection((HOST, PORT))
    # for x in range(10):
        # message = 'Hello World!:{}\n'.format(x)
        # 送信
    scrtime = time.time()
    sct_img = sct.grab(rect)
    image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    compress_data = zlib.compress(image.tobytes(),3)
    print("[cmpl]",time.time() - scrtime)

    # conn.send(message.encode('utf-8', 'ignore'))
    sendtime = time.time()
    # conn.sendall(str(compress_data).encode())
    conn.sendall(str(compress_data[:1000]).encode())
    len_compless = len(compress_data)
    print("[len ]",len(compress_data))
    # for i in range(len_compless):
    #     if i % 2999 == 0:
    #         conn.sendall(str(compress_data[:3000]).encode())
    #         compress_data = compress_data[3000:]

    print("[send]",time.time() - sendtime)
    print("[ALL ]",time.time() - scrtime)
        # recv_message = conn.recv(3000)
        # print('recv:' + len(recv_message.decode()))
        # 1秒待つ
    conn.close()


def main():
    for x in range(1):
        # jobs = [gevent.spawn(client) for x in range(100)]
        jobs = [gevent.spawn(client)]
        gevent.joinall(jobs)
        print("==============")


main()
