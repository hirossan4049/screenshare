import os
import subprocess
import tempfile

from PIL import ImageGrab
import time
from mss import mss

# full screen
# start = time.time()
# fh, filepath = tempfile.mkstemp(".png")
# os.close(fh)
# subprocess.call(["screencapture", "-x", filepath])
# os.unlink(filepath)
# elapsed_time = time.time() - start
# print(elapsed_time)

# start = time.time()
# ImageGrab.grab().save("PIL_capture.png")
# elapsed_time = time.time() - start
# print(l)

start = time.time()
# The simplest use, save a screen shot of the 1st monitor
with mss() as sct:
    sct.shot()
elapsed_time = time.time() - start
print(elapsed_time)