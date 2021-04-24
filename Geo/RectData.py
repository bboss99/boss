from __future__ import annotations
from .. utils import _addCallback
from copy import copy as copy_copy
from math import copysign

__all__ = ['RectData']

class RectData():
    def __init__(self, xMin=0, yMin=0, width=0, height=0):
        self.xMin = xMin
        self.yMin = yMin
        self.width = width
        self.height = height

        self.xMax = self.xMin + self.width
        self.yMax = self.yMin + self.height

        self.onUpdate = []

    def __str__(self):
        return ("( xMin,yMin,width,height -  {} , {} , {} , {} )".format(self.xMin, self.yMin, self.width, self.height))

    @property
    def center(self):
        return (self.xMin + self.xMax)/2, (self.yMin + self.yMax)/2

    @classmethod
    def from_minMax(cls, xMin, yMin, xMax, yMax):
        return cls(xMin, yMin, xMax - xMin, yMax - yMin)

    @classmethod
    def from_object(cls, rectData):
        return cls(rectData.xMin, rectData.yMin, rectData.width, rectData.height)

    @classmethod
    def centeredAt(cls, centerX, centerY, width, height):
        return cls(int(centerX - width / 2), int(centerY - height / 2), width, height)

    def getTuple(self):
        return (self.xMin, self.yMin, self.width, self.height)

    def _set_clip_min_max(self):
        self._clipRect = self.getTupleMinMax()  

    def copy(self):
        return copy_copy(self)

    def getTupleMinMax(self):
        return (self.xMin, self.yMin, self.xMax, self.yMax)

    def setPositionAndSize_fromRectData(self, rectData):
        self.setPositionAndSize(rectData.xMin, rectData.yMin, rectData.width, rectData.height)

    def setPositionAndSize_minMax(self, xMin, yMin, xMax, yMax):
        self.xMin = xMin
        self.yMin = yMin

        self.xMax = xMax
        self.yMax = yMax

        self.width = self.xMax - self.xMin
        self.height = self.yMax - self.yMin

        self._onUpdate()

    def setPositionAtCenter(self, centerX, centerY):
        self.xMin = centerX - self.width / 2
        self.xMax = centerX + self.width / 2
        self.yMin = centerY - self.height / 2
        self.yMax = centerY + self.height / 2
        self._onUpdate()

    def setPositionAndSize(self, xMin, yMin, width, height):
        self.xMin = xMin
        self.yMin = yMin

        self.width = width
        self.height = height

        self.xMax = self.xMin + self.width
        self.yMax = self.yMin + self.height

        self._onUpdate()

    def remove_onUpdate(self, func):
        for fn in self.onUpdate:
            if fn.func == func:
                self.onUpdate.remove(fn)
                break

    def add_onUpdate(self, *params):
        _addCallback(self, self.onUpdate, *params)

    def _onUpdate(self):
        for fn in self.onUpdate:
            fn()

    def setPosition(self, xMin, yMin):
        self.xMin = xMin
        self.yMin = yMin
        self.xMax = self.xMin + self.width
        self.yMax = self.yMin + self.height
        self._onUpdate()

    def isPointInside(self, x, y):
        return x > self.xMin and x < self.xMax and y > self.yMin and y < self.yMax

    def getTop(self, space=0,width=-1,height=-1,fromTop=True,count = 1):
        firstRd = RectData(
            self.xMin,
            (self.yMax if fromTop else self.yMin) + space,
            self.width if width == -1 else self.width * width if type(width) == float else width,
            self.height if height == -1 else self.height*height if type(height) == float else height
        )
        if count == 1:
            return firstRd
        else:
            return [firstRd] + [
                RectData(
                    firstRd.xMin,
                    firstRd.yMin + (space + firstRd.height)*(i+1),
                    firstRd.width,
                    firstRd.height
                ) for i in range(count -1)
            ]

    def getBottom(self, space=0,width=-1,height=-1,fromBottom=True,count=1):
        newHeight = self.height if height == -1 else self.height*height if type(height) == float else height

        firstRd = RectData(
            self.xMin,
            (self.yMin if fromBottom else self.yMax) - space - newHeight,
            self.width if width == -1 else self.width * width if type(width) == float else width,
            newHeight
        )

        if count == 1:
            return firstRd
        else:
            return [firstRd] + [
                RectData(
                    firstRd.xMin,
                    firstRd.yMin - (space + newHeight)*(i+1),
                    firstRd.width,
                    newHeight
                ) for i in range(count-1)
            ]

    def getRight(self, space=0, width=-1, height=-1,fromRight=True,count = 1):
        firstRd = RectData(
            (self.xMax if fromRight else self.xMin) + space,
            self.yMin,
            self.width if width == -1 else self.width * width if type(width) == float else width,
            self.height if height == -1 else self.height*height if type(height) == float else height
        )

        if count == 1:
            return firstRd
        else:
            return [firstRd] + [
                RectData(
                    firstRd.xMin + (space + firstRd.width)*(i+1),
                    firstRd.yMin,
                    firstRd.width,
                    firstRd.height
                ) for i in range(count -1)
            ]

    def getLeft(self, space=0,width=-1,height=-1,fromLeft=True, count = 1):
        newWidth = self.width if width == -1 else self.width*width if type(width) == float else width
        firstRd = RectData(
            (self.xMin if fromLeft else self.xMax) - space - newWidth,
            self.yMin,
            newWidth,
            self.height if height == -1 else self.height*height if type(height) == float else height
        )
        if count ==1:
            return firstRd
        else:
            return [firstRd] + [
                RectData(
                    firstRd.xMin - (space + newWidth) * (i + 1),
                    firstRd.yMin,
                    newWidth,
                    firstRd.height
                ) for i in range(count - 1)
            ]

    @staticmethod
    def getRectDataGrid(rd:RectData, count:int, columnCount:int, xSpace:int, ySpace:int,xGoesRight=True,yGoesUp=False):
        rdList = []
        append = rdList.append
        for elementCount in range(count):
            elementCount = elementCount + 1  
            remainder = elementCount % columnCount
            curColumn = columnCount if remainder == 0 else remainder

            if xGoesRight:
                newXMin = rd.xMin + (xSpace + rd.width) * (curColumn - 1)
            else:
                newXMin = rd.xMin - (xSpace + rd.width) * (curColumn - 1)

            division = int((elementCount - 1) / columnCount)

            if yGoesUp:
                newYMin = rd.yMin + (ySpace + rd.height) * division
            else:
                newYMin = rd.yMin - (ySpace + rd.height) * division

            r = RectData(
                newXMin,
                newYMin,
                rd.width,
                rd.height
            )
            append(r)

        return rdList

    def getScaled(self, width=1,height=1,scaleAnchor='bl'):
        '''
        floats.
        '''
        if type(scaleAnchor) == str:
            if scaleAnchor == 'bl':
                scaleAnchor = (self.xMin,self.yMin)
            elif scaleAnchor == 'left':
                scaleAnchor = (self.xMin, (self.yMin+self.yMax)/2)
            elif scaleAnchor == 'tl':
                scaleAnchor = (self.xMin, self.yMax)
            elif scaleAnchor == 'top':
                scaleAnchor = ((self.xMin + self.xMax) / 2, self.yMax)
            elif scaleAnchor == 'tr':
                scaleAnchor = (self.xMax, self.yMax)
            elif scaleAnchor == 'right':
                scaleAnchor = (self.xMax, (self.yMin+self.yMax)/2)
            elif scaleAnchor == 'br':
                scaleAnchor = (self.xMax,self.yMin)
            elif scaleAnchor == 'bottom':
                scaleAnchor = ((self.xMin + self.xMax) / 2, self.yMin)
            elif scaleAnchor == 'center':
                scaleAnchor = ((self.xMin + self.xMax) / 2, (self.yMin+self.yMax)/2)

        dx = scaleAnchor[0]
        dy = scaleAnchor[1]

        new_xMin = (self.xMin - dx)*width  + dx
        new_xMax = (self.xMax - dx)*width  + dx
        new_yMin = (self.yMin - dy)*height + dy
        new_yMax = (self.yMax - dy)*height + dy

        return RectData.from_minMax(
            new_xMin,
            new_yMin,
            new_xMax,
            new_yMax
        )

    def expandShrinkRect(self, inX, inY):
        return RectData(
            self.xMin - inX / 2,
            self.yMin - inY / 2,
            self.width + inX,
            self.height + inY
        )

    @staticmethod
    def unionRectDataList(rectDataList):
        if len(rectDataList) < 1:
            return RectData(0, 0, 0, 0)

        else:
            u_xMin = rectDataList[0].xMin
            u_xMax = rectDataList[0].xMax
            u_yMin = rectDataList[0].yMin
            u_yMax = rectDataList[0].yMax

            for rd in rectDataList[1:]:
                u_xMin = min(u_xMin, rd.xMin)
                u_yMin = min(u_yMin, rd.yMin)
                u_xMax = max(u_xMax, rd.xMax)
                u_yMax = max(u_yMax, rd.yMax)

            return RectData.from_minMax(u_xMin, u_yMin, u_xMax, u_yMax)

    @staticmethod
    def isRectDataOutside(rd1:RectData, rd2:RectData):
        return rd2.xMin > rd1.xMax or rd2.xMax < rd1.xMin or rd2.yMin > rd1.yMax or rd2.yMax < rd1.yMin

    @staticmethod
    def intersectRectData(rd1, rd2):
        x1, y1, X1, Y1 = rd1.getTupleMinMax()
        x2, y2, X2, Y2 = rd2.getTupleMinMax()

        return RectData.from_minMax(
            max(x1, x2),
            max(y1, y2),
            min(X1, X2),
            min(Y1, Y2)
        )

    @staticmethod
    def clipRectData(innerRD,outerRD=None,uip=None):
        if outerRD == None:
            outerRD = RectData(0,0,uip.region_width,uip.region_height)

        clippedRD = RectData.from_minMax(
                            max(outerRD.xMin,innerRD.xMin),
                            max(outerRD.yMin,innerRD.yMin),
                            min(outerRD.xMax,innerRD.xMax),
                            min(outerRD.yMax,innerRD.yMax)
                        )
        return clippedRD
