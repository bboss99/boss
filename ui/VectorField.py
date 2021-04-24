from ..Geo.RectData import RectData
from . Panel import Panel,PanelData
from .. Text import TextData, Text
from . CheckBox import CheckBox
from . Button import Button,ButtonData
from .. Color import Color
from . FloatField import FloatField
from . IntField import IntField
from itertools import chain
from .. utils import _addCallback,appendCheck

__all__ = ['VectorFloatField','VectorIntField','VectorBooleanField']

class _VectorField():
    def __init__(self, op, rectData=None,panelData=None,bgPanelData=None,value= None,
                 minValue = None, maxValue = None, changeBy = None,isHorizontal = True,fieldGap = .1,
                 onTextChange=None, onValueChange=None, onEnterPress = None, param = None):
        self.op             = op

        self.param          = param
        self.isHorizontal   = isHorizontal
        self.fieldGap       = fieldGap  

        self.panelData      = panelData if panelData else PanelData()
        
        self.basePanel      = Button(
                                op              = op,
                                rectData        = rectData,

                                panelData       = bgPanelData if bgPanelData else PanelData(panelType='VectorBG'),
                                buttonData      = ButtonData()
                            )

        self.rectData       = self.basePanel.rectData
  
        xRd,yRd,zRd         = self._getFieldsPositions()
        
        xPd                 = self.panelData.copy()        
        xPd.parent          = self.basePanel
        xPd.canDrag         = False
        xPd.rectIsLocal     = False

        yPd                 = self.panelData.copy()
        yPd.parent          = self.basePanel
        yPd.canDrag         = False
        yPd.rectIsLocal     = False

        zPd                 = self.panelData.copy()
        zPd.parent          = self.basePanel
        zPd.canDrag         = False
        zPd.rectIsLocal     = False

        if type(self) == VectorBooleanField:
            self._T               = CheckBox
            self.x_field   = CheckBox(
                                    op              = op,
                                    rectData        = xRd,
                                    panelData       = xPd,
                                    value           = value[0],
                                )

            self.y_field   = CheckBox(
                                    op              = op,
                                    rectData        = yRd,
                                    panelData       = yPd,
                                    value           = value[1],
                                )

            self.z_field   = CheckBox(
                                    op              = op,
                                    rectData        = zRd,
                                    panelData       = zPd,
                                    value           = value[2],
                                )
        else:
            if type(self) == VectorIntField:
                self._T         = IntField
                if changeBy is not None:
                    cb = changeBy
                else:
                    cb = (1, 1, 1)
            else:
                self._T = FloatField
                if changeBy is not None:
                    cb = changeBy
                else:
                    cb = (.1, .1, .1)

            if minValue is not None:
                minv = minValue
            else:
                minv = (None, None, None)

            if maxValue is not None:
                maxv = maxValue
            else:
                maxv = (None, None, None)

            self.x_field   = self._T(
                                    op              = op,
                                    rectData        = xRd,
                                    panelData       = xPd,
                                    value           = value[0],
                                    minValue        = minv[0],
                                    maxValue        = maxv[0],
                                    changeBy        = cb[0],
                                )

            self.y_field   = self._T(
                                    op              = op,
                                    rectData        = yRd,
                                    panelData       = yPd,
                                    value           = value[1],
                                    minValue        = minv[1],
                                    maxValue        = maxv[1],
                                    changeBy        = cb[1],
                                )

            self.z_field   = self._T(
                                    op              = op,
                                    rectData        = zRd,
                                    panelData       = zPd,
                                    value           = value[2],
                                    minValue        = minv[2],
                                    maxValue        = maxv[2],
                                    changeBy        = cb[2],
                                )

        if onTextChange:
            self.add_onTextChange(onTextChange)
        if onEnterPress:
            self.add_onEnterPress(onEnterPress)
        if onValueChange:
            self.add_onValueChange(onValueChange)

    def add_onTextChange(self, *params):
        if self._T == CheckBox:
            raise Exception('onTextChange not supported for CheckBoxes')
        else:
            _addCallback(self, self.x_field.onTextChange, *params)
            _addCallback(self, self.y_field.onTextChange, *params)
            _addCallback(self, self.z_field.onTextChange, *params)

    def add_onValueChange(self, *params):
        if self._T == CheckBox:
            _addCallback(self, self.x_field.button.onClick, *params)
            _addCallback(self, self.y_field.button.onClick, *params)
            _addCallback(self, self.z_field.button.onClick, *params)
        else:
            _addCallback(self, self.x_field.onValueChange, *params)
            _addCallback(self, self.y_field.onValueChange, *params)
            _addCallback(self, self.z_field.onValueChange, *params)

    def add_onEnterPress(self, *params):
        if self._T == CheckBox:
            raise Exception('onEnterPress not supported for CheckBoxes')
        else:
            _addCallback(self, self.x_field.onEnterPress, *params)
            _addCallback(self, self.y_field.onEnterPress, *params)
            _addCallback(self, self.z_field.onEnterPress, *params)

    @property
    def value(self):
        return self.x_field.value, self.y_field.value, self.z_field.value

    @property
    def text(self):
        if self._T == CheckBox:
            return self.value
        return self.x_field.text, self.y_field.text, self.z_field.text

    def _getFieldsPositions(self):
        rectData = self.basePanel.rectData
              
        _fieldGapPxl   =  rectData.width * self.fieldGap            
        _fieldWidth    = (rectData.width - _fieldGapPxl * 4)/3

        rdX = RectData(rectData.xMin + _fieldGapPxl ,rectData.yMin, _fieldWidth, rectData.height)
        
        rdY = RectData(
            rectData.xMin + _fieldGapPxl*2 + _fieldWidth,
            rectData.yMin,
            _fieldWidth,
            rectData.height
        )
                
        rdZ = RectData(
            rectData.xMin + _fieldGapPxl*3 + _fieldWidth*2,
            rectData.yMin,
            _fieldWidth,
            rectData.height
        )
        
        return rdX,rdY,rdZ

    def setPositionAndSize(self,rectData):
        xRd,yRd,zRd         = self._getFieldsPositions()
        if self.isHorizontal:
            self.x_field.button.setPositionAndSize_fromRectData(xRd)
            self.y_field.button.setPositionAndSize_fromRectData(yRd)
            self.z_field.button.setPositionAndSize_fromRectData(zRd)                

    def getPanels(self):
        return []

    def getButtons(self):
        return [self.basePanel] + self.x_field.getButtons() + self.y_field.getButtons() + self.z_field.getButtons()

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

class VectorFloatField(_VectorField):
    def __init__(self, op, rectData=None, panelData=None, bgPanelData=None, value=(0.0, 0.0, 0.0),
                 minValue = None,maxValue = None,changeBy = (.1,.1,.1),isHorizontal=True,
                 fieldGap=.1, onTextChange=None, onValueChange=None, onEnterPress=None, param=None):
        _VectorField.__init__(self, op, rectData, panelData, bgPanelData, value,minValue,maxValue,changeBy,isHorizontal, fieldGap, onTextChange,
                              onValueChange, onEnterPress, param)

class VectorIntField(_VectorField):
    def __init__(self, op, rectData=None, panelData=None, bgPanelData=None, value=(0, 0, 0),
                 minValue = None,maxValue = None,changeBy = (1,1,1), isHorizontal=True,
                 fieldGap=.1, onTextChange=None, onValueChange=None, onEnterPress=None, param=None):
        _VectorField.__init__(self, op, rectData, panelData, bgPanelData, value,minValue,maxValue,changeBy, isHorizontal, fieldGap, onTextChange,
                              onValueChange, onEnterPress, param)

class VectorBooleanField(_VectorField):
    def __init__(self, op, rectData=None, panelData=None, bgPanelData=None, value=(True, True, True), isHorizontal=True,
                 fieldGap=.1, onValueChange=None, param=None):
        _VectorField.__init__(self, op, rectData, panelData, bgPanelData, value,None,None,None,isHorizontal, fieldGap, None,
                              onValueChange, None, param)

