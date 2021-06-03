import cv2


class video():
    def __init__(self, type):
        if type == 0:
            self.video = cv2.VideoCapture('./video/cat_video.mp4')
        else:
            self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        run, frame = self.video.read()
        img = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
        ret, jpg_img = cv2.imencode('.jpg', frame)
        return jpg_img.tobytes()
