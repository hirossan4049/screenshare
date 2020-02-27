import time
import zlib

import Quartz
# import pyautogui as pyautogui
import cv2
import numpy
from mss import mss
from PIL import Image, ImageChops

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

# pyautogui.size()
size = Quartz.CGDisplayPixelsWide(Quartz.CGMainDisplayID()), Quartz.CGDisplayPixelsHigh(Quartz.CGMainDisplayID())
sizepos = 0,0,size[0],size[1]
print(sizepos)

def main():
    with mss() as sct:
        print(sizepos)
        shot = sct.grab(sizepos)
        cashe_img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")

        # for i in range(100):
        #     shot = sct.grab(size)
        #     image = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        #     # print(shot.bgra)
        #     print(len(image.tobytes()))
        #     difference = ImageChops.difference(image,cashe_img).getbbox()
        #     print(difference)
        #     cashe_img = image


def diffence():
    with mss() as sct:
        print("SIZE:",size)
        shot1 = numpy.array(sct.grab(sizepos))
        shot1 = cv2.resize(shot1,size)
        time.sleep(1)
        t = time.time()
        shot2 = numpy.array(sct.grab(sizepos))
        shot2 = cv2.resize(shot2,size)



    fgbg = cv2.createBackgroundSubtractorMOG2()
    fgmask0 = fgbg.apply(shot1)
    fgmask = fgbg.apply(shot2)

    # img_msk2 = cv2.cvtColor(fgmask, cv2.COLOR_BGR2GRAY)

    dst = cv2.bitwise_or(shot2,shot2,mask=fgmask)
    print("時間　:",time.time()-t)

    print("元画像:",len(shot2.tostring()))
    print("処理後:",len(dst.tostring()))
    print("==========")
    comp = zlib.compress(shot2.tostring(),5)
    comp2 = zlib.compress(dst.tostring(),5)
    print("前圧縮",len(comp))
    print("後圧縮",len(comp2))

    # print(new)


    # dst = cv2.add(shot2,fgmask)
    # 表示
    # cv2.imshow('frame',fgmask)

    # 検出画像
    print("saving now....")
    # bg_diff_path  = './diff.jpg'
    # cv2.imwrite(bg_diff_path,fgmask)
    print(shot2.shape)
    cv2.imwrite("diff.png",fgmask)
    cv2.imwrite("result.png",dst)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
# main()




def diffenceloop():
    fgbg = cv2.createBackgroundSubtractorMOG2()
    cashe_shot = None
    with mss() as sct:
        for _ in range(10):
            print("SIZE:",size)
            shot = numpy.array(sct.grab(sizepos))
            shot = cv2.resize(shot,size)
            fgmask = fgbg.apply(shot)

            try:
                dst = cv2.bitwise_or(cashe_shot,shot,mask=fgmask)
            except:
                print("except")
                cashe_shot = shot
    cv2.imwrite("diffenceloop.png",dst)



# diffence()
diffenceloop()