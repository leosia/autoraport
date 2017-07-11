# -*- coding: UTF-8 -*-

import cv2
import numpy as np

class Video():
    def video_cutter(self):
        video = cv2.VideoCapture('video.avi')
        counter = 0

        while(video.isOpened()):
            ret, frame = video.read()
            filename = 'img' + str(counter) + '.jpg'
            if ret == True:
                # cv2.imshow('frame', frame)
                cv2.imwrite(filename, frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
            counter += 1

        video.release()
        cv2.destroyAllWindows()

v = Video()
v.video_cutter()
