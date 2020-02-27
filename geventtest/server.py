# -*- coding: utf-8 -*-
import time

from gevent.pool import Pool
from gevent.server import StreamServer
import socket as py_socket
from gevent.socket import wait_read, wait_write


class TooLong(Exception):
    pass


def handle(socket, address):
    print('new connection!')
    fp = socket.makefile()
    try:
        _prev_message = ""
        while True:
            wait_read(socket.fileno(), timeout=5, timeout_exc=TooLong)
            line = fp.readline()

            if line:
                print("[wait]", time.time())

                # 前回受信分を含めた応答文字列を生成
                s = _prev_message + line
                print("==========")
                print(len(s))
                # 送信
                # socket.send(s.encode('utf-8', 'ignore'))
                # fp.flush()
                _prev_message = line
    except TooLong:
        print('timeout')

    # Timeoutが発生したら切断する
    socket.shutdown(py_socket.SHUT_RDWR)
    socket.close()


pool = Pool(10000)  # do not accept more than 10000 connections
server = StreamServer(('127.0.0.1', 1234), handle, spawn=pool)
server.serve_forever()