import time

import cv2
import numpy
from PIL import Image
from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import Line
from kivy.graphics import Ellipse
from mss import mss
import Quartz.CoreGraphics as CG

WIDTH = 1920
HEIGHT = 1200


# WIDTH = 3840
# HEIGHT = 2400

class MyApp(App):
    title = 'Simple Graphics'

    def build(self):
        self.widget = Widget()
        self.sct = mss()
        self.rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}
        self.fgbg = cv2.createBackgroundSubtractorMOG2()

        self.texture = Texture.create(size=(WIDTH, HEIGHT))

        Clock.schedule_interval(self.update, 0)

        return self.widget

    def update(self, _):
        region = CG.CGRectInfinite

        # Create screenshot as CGImage
        t = time.time()

        image = CG.CGWindowListCreateImage(
            region,
            CG.kCGWindowListOptionOnScreenOnly,
            CG.kCGNullWindowID,
            CG.kCGWindowImageDefault)

        bytesperrow = CG.CGImageGetBytesPerRow(image)

        pixeldata = CG.CGDataProviderCopyData(CG.CGImageGetDataProvider(image))
        image = numpy.frombuffer(pixeldata, dtype=numpy.uint8)
        image = image.reshape((2400, bytesperrow // 4, 4))
        # image = image[:, :width, :]
        im_rgb = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        image = cv2.flip(im_rgb, 0)
        image = cv2.resize(image, (1920, 1200))

        # pilimage = Image.fromarray(image)
        # print(pilimage.size)
        # cv2.imwrite("CG.png",image)
        fgmask = self.fgbg.apply(image)
        #
        dst = cv2.bitwise_or(image, image, mask=fgmask)
        # image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        # imgdata=numpy.fromstring(_data,dtype=numpy.uint8).tobytes()
        # image = image.resize((int(image.width / 2), int(image.height / 2)))
        self.texture.blit_buffer(dst.tobytes(), colorfmt='rgb')
        with self.widget.canvas:
            Rectangle(texture=self.texture, pos=(0, 0), size=Window.size)
        print(time.time() - t)


if __name__ == '__main__':
    MyApp().run()
