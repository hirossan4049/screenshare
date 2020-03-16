from mss import mss
import numpy
import cv2
import time
# import threading
import concurrent.futures
# from multiprocessing.pool import ThreadPool



sct = mss()
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1200}

def sct_func():
    img = numpy.array(sct.grab(monitor))
    height = img.shape[0]
    width = img.shape[1]
    resized_img = cv2.resize(img,(width // 4, height//4))

    return resized_img

# while True:
t = time.time()


# for _ in range(30):
#     # thread1 = threading.Thread(target=sct_func)
#     # thread1.start()
#     async_result = pool.apply_async(sct_func)
#     return_val = async_result.get()  # get the return value from your function.
#
#
#     # print("TASK NOW")
#     time.sleep(1/30)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    for _ in range(120):
        future = executor.submit(sct_func)
        print(future.result())

        # cv2.imshow('client',future.result())
        # cv2.waitKey(0)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        time.sleep(1/60)

print(time.time() - t)
print("END")
