from PIL import ImageGrab
from mss import mss
import time

t = time.time()

img = ImageGrab.grab()

print(time.time() - t)

t = time.time()
with mss as sct:
    sct.grab({'top': 0, 'left': 0, 'width': 1920, 'height': 1200})
print(time.time() - t)
