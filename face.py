import math
import cv2


class Face:
    KNOWN_WIDTH = 16.0
    KNOWN_DISTANCE = 25.0

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.x_end = x + w
        self.y_end = y + h

        self.x_mid = math.floor((self.x + self.x_end) / 2)
        self.y_mid = math.floor((self.y + self.y_end) / 2)

        self.isMask = False
        self.box_color = (0, 255, 0)
        if self.isMask:
            self.box_color = (0, 0, 255)

        # Camera Focal Length
        F = (300 * 29) / 16
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.est_dist = round((16 * F) / w, 2)
        self.x_mid_inches = (self.x_mid * self.est_dist) / F
        self.y_mid_inches = (self.y_mid * self.est_dist) / F
