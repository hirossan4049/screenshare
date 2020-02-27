import socket
import zlib

PORT = 50001
BUFFER_SIZE = 1024
from PIL import Image
from mss import mss
import time

WIDTH = 1920
HEIGHT = 1080
rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', PORT))
    with mss() as sct:
        for i in range(100):
            sct_img = sct.grab(rect)
            image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            compress_data = zlib.compress(image.tobytes(), 5)
            print(len(compress_data))
            t = time.time()
            s.sendall(compress_data)
            print(time.time() - t)
    # data = input('Please input > ')
    # s.send(data.encode())