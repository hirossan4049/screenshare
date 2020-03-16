#!/usr/local/bin/python3

import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code
import time
import zlib


cap=cv2.VideoCapture(1)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8089))
while True:
    readt = time.time()
    ret,frame=cap.read()
    print(len(frame))
    readtime = time.time() - readt

    picklet = time.time()
    data = pickle.dumps(frame) ### new code
    pickletime = time.time() - picklet

    print(data[:30])
    print(len(data))
    sendt = time.time()
    compdata = zlib.compress(data)
    clientsocket.sendall(struct.pack("L", len(data))+compdata)
    sendtime = time.time() - sendt

    print("SENDEND")
    print("[READ]",readtime)
    print("[PICK]",pickletime)
    print("[SEND]",sendtime)
    # time.sleep(1)

    cv2.imshow('client',frame)
    # cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
