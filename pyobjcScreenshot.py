from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout

Config.set('graphics', 'fullscreen', 0)

from PIL import Image
from mss import mss
import time

WIDTH = 1920
HEIGHT = 1080
rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

with mss() as sct:
    for i in range(100):
        t = time.time()
        sct_img = sct.grab(rect)
        image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        image.tobytes()
        print(time.time() - t)
