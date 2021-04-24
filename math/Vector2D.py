
from math import sqrt, sin,cos,pi,acos,degrees,atan2,radians

class Vector2D():
    def __init__(self,x,y):
        self.x          = x
        self.y          = y
        self.magnitude  = self._getMagnitude()

    def _getMagnitude(self):
        return sqrt( self.x*self.x + self.y*self.y )
    
    def normalized(self):        
        return Vector2D(self.x/self.magnitude, self.y/self.magnitude)

    @classmethod
    def from_tuple(cls,point):
        return cls( point[0], point[1] )

    @staticmethod
    def rotate_point(center,point,angle):
        angle = radians(angle)
        cos_angle = cos(angle)
        sin_angle = sin(angle)
        return Vector2D(
            cos_angle * (point.x - center.x) - sin_angle * (point.y - center.y) + center.x,
            sin_angle * (point.x - center.x) + cos_angle * (point.y - center.y) + center.y
            )

    def to_tuple(self):
        return (self.x,self.y)

    def rotate(self,angle):
        angle = radians(angle)
        cos_angle = cos(angle)
        sin_angle = sin(angle)
        
        new_x = cos_angle * self.x - sin_angle * self.y
        new_y = sin_angle * self.x + cos_angle * self.y

        self.x = new_x
        self.y = new_y
                
        self.magnitude = self._getMagnitude()
    
    @staticmethod
    def dot(a,b):
        return ( a.x * b.x + a.y * b.y )
    
    @staticmethod
    def angle(a,b):
        return atan2(b.y,b.x) - atan2(a.y,a.x)

    def normalize(self):
        self.x = self.x/self.magnitude
        self.y = self.y/self.magnitude

        self.magnitude = self._getMagnitude()

    @staticmethod
    def getAnchorVectors(rectData,keys=False):
        xCenter = (rectData.xMin + rectData.xMax) / 2
        yCenter = (rectData.yMin + rectData.yMax) / 2
        vectors =  [
            Vector2D(xCenter, rectData.yMin),
            Vector2D(rectData.xMin, rectData.yMin),
            Vector2D(rectData.xMin, yCenter),
            Vector2D(rectData.xMin, rectData.yMax),
            Vector2D(xCenter, rectData.yMax),
            Vector2D(rectData.xMax, rectData.yMax),
            Vector2D(rectData.xMax, yCenter),
            Vector2D(rectData.xMax, rectData.yMin),
            Vector2D(xCenter, yCenter)
        ]
        if keys:
            from ..Alignment import Align
            keys = (
                Align.Bottom,Align.BL,Align.Left,Align.TL,
                Align.Top,Align.TR,Align.Right,Align.BR,
                Align.Center
            )
            return [ (k,v)for k,v in zip(keys , vectors) ]
        else:
            return vectors

    def __add__(self, other): 
        return Vector2D(self.x + other.x,self.y +other.y)

    def __sub__(self, other): 
        return Vector2D(self.x - other.x,self.y - other.y)
    
    def __mul__(self, other):        
        return Vector2D(self.x*other,self.y*other)

    def __str__(self):
        return '({} , {} , magnitude - {})'.format( self.x, self.y, self.magnitude )

def rotate_point(center,point,angle):
    angle = radians(angle)
    cx = center[0]
    cy = center[1]
    
    px = point[0]
    py = point[1]

    return (
        cos(angle) * (px - cx) - sin(angle) * (py - cy) + cx,
        sin(angle) * (px - cx) + cos(angle) * (py - cy) + cy
        )


