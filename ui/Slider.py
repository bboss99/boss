from ..Geo.RectData import RectData
from . Panel import Panel,PanelData
from . Button import Button,ButtonData
from functools import partial
from .. Color import Color
from .. utils import _addCallback
from itertools import chain
__all__ = ['Slider']

class Slider():   
    def __init__(self,op,rectData=None,panelData=None,value=0, minValue=0, maxValue=1,
                        isHorizontal=True,onValueChange = None,
                        barSizeFactor = .1,  reverse=False,
                    ):
        self.op                     = op
        self.value                  = value 
        self.minValue               = minValue
        self.maxValue               = maxValue
        self.isHorizontal           = isHorizontal
        self.barSizeFactor          = barSizeFactor
        self.reverse                = reverse

        panelData                   = panelData if panelData else PanelData()

        panelData.panelType         = 'SliderBase'

        panelData.canDrag           = False
        
        self.sliderBase             = Button(
                                        op,
                                        rectData, 
                                        panelData,
                                        ButtonData()
                                        )
        
        self.sliderBar              = Button(
                                        op,
                                        RectData(),
                                        PanelData(
                                            parent = self.sliderBase,
                                            dragRect= self.sliderBase.rectData,
                                            panelType='SliderBar'
                                            ),
                                        ButtonData()
                                        )
        self.onValueChange          = []

        self.add_onValueChange(onValueChange)

        self.sliderBar.add_onDrag(self.setValueFromLocation)
        
        self.sliderBase.add_onWheelUp( self._updateValue, (self.maxValue - self.minValue)/10 )
        self.sliderBase.add_onWheelDown( self._updateValue, -(self.maxValue - self.minValue)/10 )        
        
        self._setBarPositionAndSize()

    def add_onValueChange(self,*params):
        _addCallback(self,self.onValueChange,*params)

    def _setBarPositionAndSize(self):
        baseRectData    = self.sliderBase.rectData        
        self.sliderBar.setPositionAndSize(
                        baseRectData.xMin,
                        baseRectData.yMin,
                        baseRectData.width *(self.barSizeFactor if self.isHorizontal else 1),
                        baseRectData.height*(1 if self.isHorizontal else self.barSizeFactor)
        )

    def setPositionAndSize(self,rectData):
        self.sliderBase.setPositionAndSize_fromRectData(rectData)
        self._setBarPositionAndSize()        

    def getValue(self):
        return self.value
    
    def _updateValue(self, updateBy,callCallback=True):
        self.setValue(self.getValue() + updateBy,callCallback)
    
    def setValue(self,value,callCallback=True):
        self.value = max(min(value,self.maxValue), self.minValue)
        
        self.setLocationFromValue()
        if callCallback:
            self._onValueChange()

    def setLocationFromValue(self):
        factor = (self.value - self.minValue) / (self.maxValue - self.minValue) 

        if self.reverse : factor = 1 - factor

        if self.isHorizontal:
            newXMin = self.sliderBase.xMin + (self.sliderBase.width - self.sliderBar.width) * factor
            self.sliderBar.setPosition(newXMin,self.sliderBar.yMin)
        else:
            newYMin = self.sliderBase.yMin + (self.sliderBase.height - self.sliderBar.height) * factor
            self.sliderBar.setPosition(self.sliderBar.xMin,newYMin)

    def setValueFromLocation(self,*args):
        if self.isHorizontal:
            factor = (self.sliderBar.xMin - self.sliderBase.xMin)/(self.sliderBase.width - self.sliderBar.width) 
            if self.reverse : factor = 1 - factor
            self.value = self.minValue + (self.maxValue - self.minValue)*factor
        else:
            factor = (self.sliderBar.yMin - self.sliderBase.yMin)/(self.sliderBase.height - self.sliderBar.height) 
            if self.reverse : factor = 1 - factor
            self.value = self.minValue + (self.maxValue - self.minValue)*factor
        
        self._onValueChange()

    def _onValueChange(self):
        for fn in self.onValueChange:
            fn()

    @property
    def dragRect(self):
        return self.sliderBar.dragRect

    def getPanels(self):
        return []

    def getButtons(self):
        return [self.sliderBase,self.sliderBar]

    def setEnabledState(self, enableState = True, pCallbacks=True, pDrawable = True):
        
        if enableState:
            self.enable(pCallbacks,pDrawable)
        else:
            self.disable(pCallbacks,pDrawable)
    
    def enable(self,pCallbacks=True,pDrawable = True):
        for each in chain(self.getPanels(), self.getButtons()):
            each.enable(pCallbacks,pDrawable)

    def disable(self,pCallbacks=True,pDrawable = True):
        for each in chain(self.getPanels(), self.getButtons()):
            each.disable(pCallbacks,pDrawable)

