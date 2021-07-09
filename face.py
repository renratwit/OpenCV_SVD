class Face:
    def __init__(self, x, y, w, h, dist):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dist = dist

        self.x_end = x + w
        self.y_end = y + h
