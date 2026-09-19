class Point:
    cnt = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        Point.cnt += 1

    def characteristic(self):
        print("x:", self.x, "\ny:", self.y, "\ncount of point:", Point.cnt)


p1 = Point()
p1.characteristic()
p2 = Point(3, 4)
p2.characteristic()
