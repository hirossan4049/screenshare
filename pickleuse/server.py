import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib


HOST='localhost'
PORT=8089

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

### new
data = bytes()
payload_size = struct.calcsize("L")
while True:
    print("WHILESTART")
    while len(data) < payload_size:
        data += conn.recv(4096)
    print("payload end")
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
        # print("msg now loading")
    print("msg_size end")
    frame_data = data[:msg_size]
    data = data[msg_size:]
    ###
    decompdata = zlib.decompress(frame_data)
    frame=pickle.loads(decompdata)
    print("FRAME",frame)
    print("END")

    cv2.imshow('frame',frame)
    # cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
