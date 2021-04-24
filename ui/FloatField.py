
from .. import utils
from .. Color import Color
from . TextField import TextField
from .base_ui.PanelData import PanelData

__all__ = ['FloatField']

class FloatField(TextField):
    def __init__(   self,
                    op,
                    rectData,panelData=None,
                    value=0.0,minValue = None,maxValue = None,changeBy = .1,precision = 3,onTextChange=None,onValueChange=None,onEnterPress = None,
                    active_color = Color.GRAY_M03, param=None):       
        
        self._formater  = "{:." + str(precision) + "f}"
        value = float(self._formater.format(utils.Float(value)))

        self.minValue   = minValue
        self.maxValue   = maxValue
        self.changeBy   = changeBy  

        panelData       = panelData if panelData else PanelData()  

        if type(self) == FloatField:
            panelData.panelType     = 'FloatField'

        TextField.__init__(self, op, rectData, panelData, value, onTextChange, onValueChange, onEnterPress,
                           active_color)

        self.param              = param
        self.op                 = op

        self._increaseBy = (self.maxValue - self.minValue)*changeBy if (minValue and maxValue) else changeBy

        self.button.add_onWheelUp(self.changeValue, self._increaseBy)
        self.button.add_onWheelDown(self.changeValue, -self._increaseBy)

    def changeValue(self, param):
        val = self.value + param  
        self._commitFloatToValue(val)
    
    def _commitTextToValue(self, pValue):
        self._commitFloatToValue(self._evaluateText(pValue))  
    
    def _commitFloatToValue(self,pValue):
        value = float(self._formater.format(pValue))
        value = self._constrainValue(value)
        if value == self.value:
            if self.text != str(self.value):
                self.text   = str(self.value) 
                self._changeTextGeo()
        else:
            self._setValueSimple(value)
            for each in self.onValueChange:
                each()

    def _constrainValue(self,value):
        if self.minValue is not None:
            value = max(value,self.minValue)
        if self.maxValue is not None:
            value = min(value,self.maxValue)
        return value

    def _evaluateText(self,value):
        try:
            return float(eval(value))
        except:
            return self.value  

    def _setValueSimple(self,value):
        self.value  = value
        self.text   = str(self.value)  
        self._changeTextGeo()
    
    def _setValue(self,value):
        self.value  = utils.Float(value)
        self.text   = str(self.value)  
        self._changeTextGeo()

    def setValue(self, value):
        try:
            newValue = float(value)
        except ValueError:
            newValue = self.value
        if newValue == self.value:
            pass
        else:
            self.value = newValue
            self._changeTextGeo()

