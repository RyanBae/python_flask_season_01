import cv2


class video():
    def __init__(self):
        # print("__init__")
        self.video = cv2.VideoCapture('./video/cat_video.mp4')
        # self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        # cap.isOpened():
        # print("Get Frame !")
        # return 'test'
        # while self.video.isOpened():
        run, frame = self.video.read()
        img = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
        ret, jpg_img = cv2.imencode('.jpg', frame)
        return jpg_img.tobytes()
