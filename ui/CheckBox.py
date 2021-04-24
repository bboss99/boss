from . Button import Button,ButtonData
from .. utils import _addCallback,appendCheck
from . base_ui.PanelData import PanelData

__all__ = ['CheckBox']

class CheckBox():
    def __init__(self,op,rectData,panelData=None,value=True,onValueChange=None,trueColor=None,falseColor=None,param=None):
        self.op                 = op
        self.value              = value
        
        self.trueColor          = trueColor if trueColor else op.uip.curStyle["ToggleTrueColor"]  
        self.falseColor         = falseColor if falseColor else op.uip.curStyle["ToggleFalseColor"]  
        
        panelData               = panelData if panelData else PanelData()  

        panelData.panelType     = 'CheckBox'

        panelData.normal_color  = self.trueColor if self.value else self.falseColor

        buttonData              = ButtonData(onClick=self._invertVal)

        self.button             = Button(op,rectData,panelData,buttonData)

        self.onValueChange      = onValueChange  

        if self.onValueChange:
            self.add_onValueChange(self.onValueChange)

        self.button.geo.setColor(self.trueColor if self.value else self.falseColor, 'normal')

        self.param              = param  

    def _invertVal(self):
        self.value = not self.value

        self.button.geo.setColor(self.trueColor if self.value else self.falseColor,'normal')

    def add_onValueChange(self,*params):
        if _addCallback(self, self.button.onClick, *params):
            appendCheck(self.op.uip.ui_onClick, self.button)
            self.button._partOf['ui_onClick'] = self.op.uip.ui_onClick


