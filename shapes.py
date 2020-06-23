import math
import sys

class Transformations():
    def __init__(self, moveX, moveY, alterSizeX, alterSizeY=0, rotation=0):
        self.moveX = moveX
        self.moveY = moveY
        self.alterSizeX = alterSizeX
        self.alterSizeY = alterSizeY
        self.rotation = rotation

class Shape():
    def __init__(self, x, y, color, sizeX, sizeY, transformations):
        self.x = x
        self.y = y
        self.color = color
        self.transformations = transformations

    def move(self, addX, addY):
        self.x = self.x + addX
        self.y = self.y + addY

class Polygon(Shape):
    def __init__(self, x, y, color, transformations):
        self.x = x
        self.y = y
        self.color = color
        self.points = []
        self.origPoints = []
        self.rotation = 0
        self.transformations = transformations

    def contains(self, x, y):
        inf = sys.float_info.max
        tiny = 0.00001
        inside = False
        for edge in self.edges():
            Ax, Ay = edge[0][0], edge[0][1]
            Bx, By = edge[1][0], edge[1][1]
            if Ay > By:
                Ax, Ay, Bx, By = Bx, By, Ax, Ay
            if y == Ay or y == By:
                y += tiny
            if (y > By or y < Ay or x > max(Ax, Bx)):
                continue
            if x < min(Ax, Bx):
                inside = not inside
                continue
            try:
                m_edge = (By - Ay) / (Bx - Ax)
            except ZeroDivisionError:
                m_edge = inf
            try:
                m_point = (y - Ay) / (x - Ax)
            except ZeroDivisionError:
                m_point = inf
            if m_point >= m_edge:
                inside = not inside
                continue
        return inside

    def move(self, x, y):
        for p in self.origPoints:
            p[0] = p[0] + x
            p[1] = p[1] + y
        for p in self.points:
            p[0] = p[0] + x
            p[1] = p[1] + y 

    def isOffscreen(self, screenX, screenY):
        xVals = [p[0] for p in self.points]
        yVals = [p[1] for p in self.points]
        right= max(xVals)
        left = min(xVals)
        top = min(yVals)
        bottom = max(yVals)
        return (top > screenY or bottom < 0 or right < 25 or left > 75)

    def rotate(self, degrees):
        self.rotation = (self.rotation + degrees) % 360
        rads = math.radians(self.rotation)
        cosang, sinang = math.cos(rads), math.sin(rads)
        for i in range(0, len(self.points)):
            x = self.origPoints[i][0]
            y = self.origPoints[i][1]
            tx, ty = x-self.x, y-self.y
            self.points[i][0] = (tx*cosang + ty*sinang) + self.x
            self.points[i][1] = (-tx*sinang +ty*cosang) + self.y

    def transform(self):
        self.move(self.transformations.moveX, self.transformations.moveY)
        self.rotate(self.transformations.rotation)

    def edges(self):
        edgeList = []
        for i, point in enumerate(self.points):
            p1 = point
            p2 = self.points[(i+1) % len(self.points)]
            edgeList.append([p1,p2])
        return edgeList

class Circle(Shape):
    def __init__(self, x, y, color, radius, transformations):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.transformations = transformations

    def alterSize(self, size):
        self.radius = self.radius + size
    
    def doTransform(self, moveX, moveY, alterSize):
        self.move(moveX, moveY)
        self.alterSize(alterSize)

    def transform(self):
        self.doTransform(self.transformations.moveX, self.transformations.moveY, self.transformations.alterSizeX)

    def contains(self, x, y):
        return  (x-self.x)**2 + (y - self.y)**2 < self.radius**2

    def containsInBorder(self, x, y, borderWidth):
        hyp = (x-self.x)**2 + (y - self.y)**2            
        return hyp < self.radius**2 and hyp > max(0, (self.radius-borderWidth)**2)

    def isOffscreen(self, screenX, screenY):
        right= self.x + self.radius
        left = self.x - self.radius
        top = self.y - self.radius
        bottom = self.y + self.radius
        return (top > screenY or bottom < 0 or right < 25 or left > 75)

class Rectangle(Polygon):
    def __init__(self, x, y, color, sizeX, sizeY, transformations):
        self.x = x
        self.y = y
        self.color = color
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.transformations = transformations
        self.points = [[x-sizeX/2, y-sizeY/2],[x-sizeX/2, y+sizeY/2],[x+sizeX/2, y+sizeY/2],[x+sizeX/2, y-sizeY/2]]
        self.origPoints = [[x-sizeX/2, y-sizeY/2],[x-sizeX/2, y+sizeY/2],[x+sizeX/2, y+sizeY/2],[x+sizeX/2, y-sizeY/2]]
        self.rotation = 0

    def containsWithoutRotation(self, x, y):
        centerXDist = self.sizeX / 2
        centerYDist = self.sizeY / 2
        return (x<(self.x + centerXDist) and x>(self.x-centerXDist) and y<(self.y + centerYDist) and y>(self.y-centerYDist))

    def isOffscreenWithoutRotation(self, screenX, screenY):
        centerXDist = self.sizeX / 2
        centerYDist = self.sizeY / 2
        right= self.x + centerXDist
        left = self.x - centerXDist
        top = self.y - centerYDist
        bottom = self.y + centerYDist
        return (top > screenY or bottom < 0 and right < 0 or left > screenX)

    def moveNoRotation(self):
        self.x = self.x + self.transformations.moveX
        self.y = self.y + self.transformations.moveY

    def transform(self):
        self.sizeX = self.sizeX + self.transformations.alterSizeX
        self.sizeY = self.sizeY + self.transformations.alterSizeY
        self.origPoints = [[self.x-self.sizeX/2, self.y-self.sizeY/2],[self.x-self.sizeX/2, self.y+self.sizeY/2],[self.x+self.sizeX/2, self.y+self.sizeY/2],[self.x+self.sizeX/2, self.y-self.sizeY/2]]
        Polygon.transform(self)