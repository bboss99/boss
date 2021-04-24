
from . base_ui.PanelData import PanelData
from . Button import Button,ButtonData
from .. Color import Color
from .. utils import _addCallback,removeCheckFunc
from itertools import chain

__all__ = ['ColorField']

class ColorField():
    def __init__(self,op,rectData, panelData = None, color = Color.WHITE,onColorUpdate = None,onColorAccept=None):
        self.op         = op
        self.rectData   = rectData

        panelData       = panelData if panelData else PanelData()

        panelData.panelType = 'ColorField'

        self.color      = color        

        panelData.normal_color = self.color
        
        self.button     = Button(
                                self.op,
                                self.rectData,
                                panelData,
                                ButtonData(
                                    onClick=self.showColorPicker
                                )
                            )
        
        self.onColorUpdate = []
        self.onColorAccept = []

        self.add_onColorAccept(onColorAccept)
        self.add_onColorUpdate(onColorUpdate)

    def showColorPicker(self):
        self.oldColor   = self.color

        self.op.uip.color_picker.setColor_fromRGBA(self.color)
        self.op.uip.color_picker.setIndicatorFromSelectedColor()
        
        self.op.uip.color_picker.setPosition(self.button.xMin,self.button.yMax + 10)
        
        self.op.uip.color_picker.onColorUpdate.append(self.onColorPickerUpdate)
        
        self.op.uip.color_picker_fn = self.colorPickerAccept

        self.op.uip.escapeFn.append(self.colorPickerCancel)

        self.op.uip.color_picker.setEnabledState(True)

    def colorPickerCancel(self):
        self.color = self.oldColor        
        self.button.geo.setColor(self.color)

        self.op.uip.color_picker.onColorUpdate.remove(self.onColorPickerUpdate)
        self.op.uip.color_picker_fn = None

        self.op.uip.color_picker.setEnabledState(False)
    
    def onColorPickerUpdate(self):
        self.color = self.op.uip.color_picker.colorRGBA  
        self.button.geo.setColor(self.color)

        for fn in self.onColorUpdate:
            fn()

    def colorPickerAccept(self):        
        self.color = self.op.uip.color_picker.colorRGBA  
        self.button.geo.setColor(self.color)
        
        self.op.uip.color_picker.onColorUpdate.remove(self.onColorPickerUpdate)
        self.op.uip.color_picker_fn = None
        self.op.uip.escapeFn.remove(self.colorPickerCancel) 
        self.op.uip.color_picker.setEnabledState(False)

        for fn in self.onColorAccept:
            fn()

    def add_onColorAccept(self,*params):
        _addCallback(self,self.onColorAccept,*params)

    def add_onColorUpdate(self,*params):
        _addCallback(self,self.onColorUpdate,*params)

    def remove_onColorAccept(self,func):
        removeCheckFunc(self.onColorAccept,func)

    def remove_onColorUpdate(self,func):
        removeCheckFunc(self.onColorUpdate,func)
    
    def getPanels(self):
        return []

    def getButtons(self):
        return [self.button]

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

