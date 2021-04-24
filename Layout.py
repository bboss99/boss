from.Geo.RectData import RectData
from .  Alignment import Align
from enum import Enum
from math import copysign
from .math.Vector2D import Vector2D

class LayoutType(Enum):
    NoLayout        =   0
    Vertical        =   1
    Horizontal      =   2 
    Grid            =   3

class Layout():
    def __init__(self,op,layoutType,rectData,align = Align.BL):
        self.op         = op
        self.layoutType = layoutType
        self.rectData   = rectData    
        self.align      = align 

        self.initRectData = self.rectData.copy()

        self.ui_elements = [] 

    def setInitRectData(self,rectData):
        self.rectData       = rectData          
        self.initRectData   = rectData.copy()

    def getNextRectData(self,uiElement):
        self.rectData = self._getNextRectData()

        self.ui_elements.append(uiElement)
        return self.rectData
    
    def removeUI(self,uiToRemove):
        if uiToRemove in self.ui_elements:
            self.ui_elements.remove(uiToRemove)            
        
        if len(self.ui_elements) > 0:
            self.rectData = self.ui_elements[-1].rectData
    
    def endLayout(self):
        self.op.uip.curLayout = None
    
    @staticmethod
    def verticalLayout(op,rectData, align = Align.BL, space = 10,activate=True):
        layout = VerticalLayout(op, LayoutType.Vertical,rectData,align,space)
        if activate:
            op.uip.curLayout = layout
        return layout   
        
    @staticmethod
    def horizontalLayout(op,rectData, align = Align.BL, space = 10,activate=True):
        layout = HorizontalLayout(op,LayoutType.Horizontal,rectData,align,space)
        if activate:
            op.uip.curLayout = layout
        return layout 

    @staticmethod
    def gridLayout(op,rectData, align = Align.BL, xSpace = 10, ySpace = 10,
                   xInRight=True, yInUp=False, columnCount = 4,activate=True):
        layout = GridLayout(op,LayoutType.Grid,rectData,align,xSpace,ySpace,xInRight,yInUp,columnCount)
        if activate:
            op.uip.curLayout = layout
        return layout 
    
    def _getNextRectData(self):
        pass

class VerticalLayout(Layout):
    def __init__(self,op,layoutType,rectData,align,space):
        Layout.__init__(self,op,layoutType,rectData,align)
        self.space = space

    def _getNextRectData(self):
        elementCount = len(self.ui_elements)
        newYMin = self.initRectData.yMin + (self.space + self.rectData.height ) * elementCount
        return RectData(
                    self.rectData.xMin,
                    newYMin,
                    self.rectData.width,
                    self.rectData.height
                )

    def reArrangeUi(self,initRectData):
        if not self.ui_elements:
            return

        self.initRectData       = initRectData
        
        for i, ui in enumerate(self.ui_elements):
            newYMin = self.initRectData.yMin + (self.space + self.rectData.height ) * elementCount

            ui.setPositionAndSize(            
                self.rectData.xMin,
                newYMin,
                self.rectData.width,
                self.rectData.height
            )        
        self.rectData = self.ui_elements[-1].rectData        
    
    def getRectDataList(self,count):
        rdList = []

        for elementCount in range(count):
            newYMin = self.initRectData.yMin + (self.space + self.rectData.height ) * i
            r = RectData(
                    self.initRectData.xMin,
                    newYMin,
                    self.initRectData.width,
                    self.initRectData.height
                )
            rdList.append(r)
        
        return rdList

    @staticmethod
    def GetRectDataListFrom(rectData,count,isUp=True,space=0.0):
        rds = []
        sign = 1 if isUp else -1
        for i in range(count):
            newYMin = rectData.yMin + (space + rectData.height ) * i*sign
            rds.append(
                RectData(
                    rectData.xMin,
                    newYMin,
                    rectData.width,
                    rectData.height
                )
            )
        return rds

class HorizontalLayout(Layout):
    def __init__(self,op,layoutType,rectData,align,space):
        Layout.__init__(self,op,layoutType,rectData,align)
        self.space = space

    def _getNextRectData(self):
        elementCount = len(self.ui_elements)
        newXMin = self.initRectData.xMin + (self.space + self.rectData.width ) * elementCount
        return RectData(
                    newXMin,
                    self.rectData.yMin,
                    self.rectData.width,
                    self.rectData.height
                )

    def reArrangeUi(self,initRectData):
        if not self.ui_elements:
            return

        self.initRectData       = initRectData
        
        for i, ui in enumerate(self.ui_elements):
            newXMin = self.initRectData.xMin + (self.space + self.rectData.width ) * elementCount

            ui.setPositionAndSize(            
                newXMin,
                self.rectData.yMin,
                self.rectData.width,
                self.rectData.height
            )        
        self.rectData = self.ui_elements[-1].rectData        
    
    def getRectDataList(self,count):        
        rdList = []

        for elementCount in range(count):
            newXMin = self.initRectData.xMin + (self.space + self.rectData.width ) * elementCount
            r = RectData(
                    newXMin,
                    self.initRectData.yMin,
                    self.initRectData.width,
                    self.initRectData.height
                )
            rdList.append(r)
        return rdList
    
    @staticmethod
    def GetRectDataListFrom(rectData,count,isRight=True,space=0.0):
        rds = []
        sign = 1 if isRight else -1
        for i in range(count):
            newXMin = rectData.xMin + (space + rectData.width ) * i * sign
            rds.append(
                RectData(
                    newXMin,
                    rectData.yMin,
                    rectData.width,
                    rectData.height
                )
            )
        return rds

class GridLayout(Layout):
    def __init__(self,op, layoutType, rectData,align,xSpace, ySpace,xInRight=True,yInUp=False, columnCount = 4):
        Layout.__init__(self,op,layoutType, rectData, align)

        self.xSpace = xSpace
        self.ySpace = ySpace
        self.xInRight = xInRight 
        self.yInUp = yInUp
        self.columnCount = columnCount
    
    def _getNextRectData(self):
        elementCount = len(self.ui_elements)

        remainder = (elementCount-1) % self.columnCount
        curColumn = self.columnCount if remainder == 0 else remainder
        
        xSign = 1 if self.xInRight else -1
        ySign = 1 if self.yInUp else -1

        newXMin = self.initRectData.xMin + (self.xSpace + self.rectData.width ) *(curColumn-1)*xSign

        division = int(elementCount/self.columnCount)

        newYMin = self.initRectData.yMin + (self.ySpace + self.rectData.height) *division*ySign

        return RectData(
                newXMin,
                newYMin,
                self.rectData.width,
                self.rectData.height
            )
    
    def reArrangeUi(self,initRectData):
        if not self.ui_elements:
            return

        self.initRectData       = initRectData
        
        for i, ui in enumerate(self.ui_elements):
            remainder           = (i+1) % self.columnCount
            curColumn           = self.columnCount if remainder == 0 else remainder
            
            newXMin             = self.initRectData.xMin + (self.xSpace + self.rectData.width ) *(curColumn-1)

            division            = int( i / self.columnCount )
            newYMin             = self.initRectData.yMin + (self.ySpace + copysign(self.rectData.height,self.ySpace) ) *division

            ui.setPositionAndSize(            
                newXMin,
                newYMin,
                self.rectData.width,
                self.rectData.height
            )        
        self.rectData = self.ui_elements[-1].rectData        
    
    def getRectDataList(self,count):        
        rdList = []

        for elementCount in range(count):
            elementCount = elementCount + 1 
            remainder = elementCount % self.columnCount
            curColumn = self.columnCount if remainder == 0 else remainder
            
            newXMin = self.initRectData.xMin + (self.xSpace + self.rectData.width ) * (curColumn-1)

            division = int( (elementCount - 1)/ (self.columnCount) )
            newYMin = self.initRectData.yMin + (self.ySpace + copysign(self.rectData.height,self.ySpace) ) *division

            r = RectData(
                    newXMin,
                    newYMin,
                    self.initRectData.width,
                    self.initRectData.height
                )
            rdList.append(r)
        return rdList

class CircleLayout(Layout):
    @staticmethod
    def getPointsInCircles(center,count =6,radius=.5,xScale = 1):
        center                  = center if isinstance(center,Vector2D) else Vector2D(center[0],center[1])
        firstPoint              = center + Vector2D(0,-radius)
        angleDiff               = 360/count
        rdsCenters              = [Vector2D.rotate_point(center,firstPoint,angleDiff*i) for i in range(count)]
        rds                     = [RectData.centeredAt(cen.x,cen.y,100,50) for cen in rdsCenters]
        return  rds


