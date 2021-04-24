from .Button import Button, ButtonData
from ..utils import _addCallback
from .base_ui.PanelData import PanelData
from typing import Union,Tuple,List

__all__ = ['OptionsBox']

class OptionsBox():
    def __init__(self, op, rectData, panelData=None,options:list=None,display_texts:List[str]=None,defaultIndex=0,
                 onValueChange=None,cycle_options = True, param=None):
        self.op = op
        self.options = options if options else ['default']

        self.display_texts = display_texts
        self.defaultIndex = defaultIndex
        self.cycle_options = cycle_options 

        self._count = len(self.options)
        self._index = defaultIndex

        self.onValueChange = []
        self.add_onValueChanged(onValueChange)

        panelData = panelData if panelData else PanelData.with_defaults()

        panelData.text = self.display_text

        buttonData = ButtonData(
            onClick=(self._onWheelRoll,'up'),
            onWheelUp=(self._onWheelRoll,'up'),
            onWheelDown=(self._onWheelRoll,'down')
        )

        self.button = Button(op, rectData, panelData, buttonData)
        self.param = param  

    @property
    def index(self):
        return self._index

    @property
    def value(self):
        return self.options[self.index]

    @property
    def display_text(self):
        if self.display_texts:
            return self.display_texts[self.index]
        else:
            return str(self.value)

    def _onWheelRoll(self,rollDir):
        if self.cycle_options:
            if rollDir == 'up':
                if self._index == self._count-1:
                    self._index =0
                else:
                    self._index += 1
            else:
                if self._index == 0:
                    self._index = self._count-1
                else:
                    self._index -= 1

            self._onValueChanged()

        else:
            if rollDir == 'up':
                if self._index < self._count - 1:
                    self._index +=1
                    self._onValueChanged()
            else:
                if self._index > 0:
                    self._index -=1
                    self._onValueChanged()

    def _onValueChanged(self):
        self.button._text.setText(self.display_text)
        for fn in self.onValueChange:
            fn()

    def add_onValueChanged(self, *params):
        _addCallback(self, self.onValueChange, *params)

