from ..Geo.RectData import RectData
from ..Geo.RectGeo import (
    RectGeo,
    RoundRectGeo,
    RoundTopRectGeo,
    RoundBottomRectGeo,
)

from . Panel import Panel
from . base_ui.PanelData import PanelData
from . Button import Button,ButtonData
from functools import partial
from .. Color import Color
from .. import utils
from itertools import chain
__all__ = ['Slider2']

class Slider2():
    def __init__(   self,
                    op,
                    rectData,
                    panelData = None,
                    value =0 ,
                    minValue = 0,
                    maxValue = 1,
                    isHorizontal= True,
                    onValueChange = None,
                    reverse=False,
                    ):        
        self.op                     = op
        panelData                   = panelData if panelData else PanelData.with_defaults()
        panelData.panelType    = 'Slider2'
        self.value                  = value 
        self.minValue               = minValue
        self.maxValue               = maxValue
        self.reverse                = reverse
        self.isHorizontal           = isHorizontal

        self.sliderBase             = Button(
                                        op,
                                        rectData,
                                        panelData,
                                        ButtonData(
                                            onDragBegin=(self.removeUpdateVerts,'add'),
                                            onDragEnd=(self.removeUpdateVerts,'remove'),
                                            onDrag=self.onSliderBaseDrag
                                            )
                                        )
        
        self.rectData               = self.sliderBase.rectData

        panelData.canDrag      = True
        self.sliderBase.setDragRect(self.rectData)

        self.sliderBar   = Panel(
                            op,
                            RectData(),
                            PanelData(
                                parent=self.sliderBase,
                                panelType='Slider2Bar'
                                )
                            )
        
        self.textPanel   = Panel(
                            op,
                            self.rectData,
                            PanelData(
                                text=str(self.value),
                                parent=self.sliderBase,
                                rectIsLocal=False,
                                panelType='Slider2Text'
                                )
                            )

        self.onValueChange          = []        
        self.add_onValueChange(onValueChange)
        
        self.sliderBase.add_onWheelUp( self._updateValue, (self.maxValue - self.minValue)/10 )
        self.sliderBase.add_onWheelDown( self._updateValue, -(self.maxValue - self.minValue)/10 )        
        
        self.setSliderBarFromValue()

    def setSliderBarFromValue(self):
        valuePercent = self.value / ( self.maxValue - self.minValue )  
        oneMinus    = 1 - valuePercent
        
        rd = self.sliderBase.rectData

        width   = rd.width  * (valuePercent if self.isHorizontal else 1)
        height  = rd.height * (valuePercent if not self.isHorizontal else 1)

        if self.reverse:
            width_oneMinus = rd.width - width
            height_oneMinus = rd.height - height
            
            xMin    = (rd.xMin + width_oneMinus if self.isHorizontal else rd.xMin ) if self.reverse else rd.xMin
            yMin    = (rd.yMin + height_oneMinus if not self.isHorizontal else rd.yMin ) if self.reverse else rd.yMin
            self.sliderBar.setPositionAndSize(
                xMin,
                yMin,
                width,
                height
            )
        else:
            self.sliderBar.setPositionAndSize(
                rd.xMin,
                rd.yMin,
                width,
                height
            )
    
    def setPositionAndSize(self,rectData):
        self.sliderBase.setPositionAndSize_fromRectData(rectData)

    def removeUpdateVerts(self,caller,*param):
        if param[0] == 'add':
            self.sliderBase.rectData.add_onUpdate(self.sliderBase.geo.updateVerts)
        else:
            self.sliderBase.rectData.remove_onUpdate(self.sliderBase.geo.updateVerts)
    
    def add_onValueChange(self,func,*params):
        if func:
            self.onValueChange.append(partial(func,self,*params))

    def onSliderBaseDrag(self,caller,*param):
        if not self.reverse:
            if self.isHorizontal:
                valuePercent    = (self.op.uip.mouse_x - self.sliderBase.xMin) / self.sliderBase.width
            else:
                valuePercent = (self.op.uip.mouse_y - self.sliderBase.yMin)/self.sliderBase.height
            
            value      = self.minValue + (self.maxValue - self.minValue)*valuePercent 

            self.setValue(value)

    def getValue(self):
        return self.value

    def setValue(self,value,callCallback=True):
        self.value = max( min( value,self.maxValue ), self.minValue)
        
        self.setSliderBarFromValue()

        self.textPanel._text.setText(str(self.value))

        if callCallback:
            self._onValueChange()
    
    def _updateValue(self, caller, updateBy,callCallback=True):
        self.setValue(self.getValue() + updateBy,callCallback)

    def _onValueChange(self):
        for fn in self.onValueChange:
            fn()
    
    def getPanels(self):
        return [self.sliderBar]

    def getButtons(self):
        return [self.sliderBase]
    
    def setEnabledState(self, enableState = True, pCallbacks=True, pDrawable = True):                
        if enableState:
            self.enable(pCallbacks,pDrawable)
        else:
            self.disable(pCallbacks,pDrawable)
    
    def enable(self,pCallbacks=True,pDrawable = True):
        for each in chain(self.getPanels(),self.getButtons()):
            each.enable(pCallbacks,pDrawable)

    def disable(self,pCallbacks=True,pDrawable = True):
        for each in chain(self.getPanels(),self.getButtons()):
            each.disable(pCallbacks,pDrawable)
  
