import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy
from flask import Flask, Response
import cv2
import mss
import time
import concurrent.futures


sct = mss.mss()
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1200}

def sct_func():
    img = numpy.array(sct.grab(monitor))
    height = img.shape[0]
    width = img.shape[1]
    resized_img = cv2.resize(img,(width // 4, height//4))

    ret, jpeg = cv2.imencode('.jpg', resized_img)
    return jpeg.tobytes()



class VideoCamera(object):
    def __init__(self):
        # self.video = cv2.VideoCapture(1)
        self.sct =  mss.mss()
        self.monitor = {"top": 0, "left": 0, "width": 1920, "height": 1200}
        print("INIT")

    # def __del__(self):
    #     self.video.release()

    def get_frame(self):
        # success, image = self.video.read()
        t = time.time()
        img = numpy.array(self.sct.grab(self.monitor))
        print(time.time() - t)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()


# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen(camera):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        while True:
            t = time.time()
            future = executor.submit(sct_func)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + future.result() + b'\r\n\r\n')
            print(time.time() - t)


server = Flask(__name__)
app = dash.Dash(__name__, server=server)

@server.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.layout = html.Div([
    # html.H1("Webcam Test"),
    html.Img(src="/video_feed",style={"height": "100vh"})
],style={"height": "100vh","text-align":"center","background-color":"#000"})

if __name__ == '__main__':
    app.run_server(debug=False)
