from boss.operators.Boss_OT_base_ui import Boss_OT_base_ui
from boss.ui.base_ui.PanelData import PanelData
from boss.ui.Panel import Panel
from boss.ui.Button import ButtonData, Button
from boss.Geo.RectData import RectData
from boss.Geo.RectGeo import RectGeo, RectGeoData
from boss.Alignment import Align
from boss.Text import TextData, Text
from boss.Color import Color
from boss.ui.CheckBox import CheckBox
from boss.ui.TextField import TextField
from boss.ui.IntField import IntField
from boss.ui.FloatField import FloatField
from boss.ui.VectorField import VectorIntField, VectorFloatField, VectorBooleanField
from boss.ui.ColorField import ColorField

from typing import Union, Callable, Optional

class FieldValue:
    def __init__(self, value, min=None, max=None, changeBy=None):
        self.value      = value
        self.min        = min
        self.max        = max
        self.changeBy   = changeBy

callbackType = Union[Callable,tuple,None]
uiType = Union[Panel,Button,None]
buttonDataType = Union[callbackType, ButtonData]
fieldType = Union[str, int, float, FieldValue, None]
vecFieldType = Union[tuple, FieldValue, None]
rectDataType = Union[RectData,tuple]

class UICreator:
    @staticmethod
    def rr(op: Boss_OT_base_ui)->RectData:
        return op.uip.region_rect

    @staticmethod
    def mouse_xy(op: Boss_OT_base_ui):
        return op.uip.mouse_x, op.uip.mouse_y

    @staticmethod
    def deleteAllUi(op: Boss_OT_base_ui):
        op.uip.deleteAllUi()

    @staticmethod
    def panel(op: Boss_OT_base_ui,
              rectData: rectDataType,
              text: str = '',
              ttt: str = '',
              tti: str = '',
              canDrag: bool = True,
              parent: Union[Panel, Button, None] = None,
              rectIsLocal: bool = False,
              param=None
              ) -> Panel:
        return Panel(op,
                     rectData if isinstance(rectData, RectData) else RectData(*rectData),
                     PanelData(
                         text=text,
                         toolTipText=ttt,
                         canDrag=canDrag,
                         toolTipImagePath=tti,
                         parent=parent,
                         rectIsLocal=rectIsLocal,
                     ),
                     param=param
                     )

    @staticmethod
    def button(op: Boss_OT_base_ui,
               rectData: rectDataType,
               text: str = '',
               buttonData: buttonDataType = None,
               ttt: str = '',
               tti: str = '',
               canDrag: bool = True,
               parent: uiType = None,
               rectIsLocal: bool = False,
               param=None
               ) -> Button:

        if isinstance(buttonData, (tuple, Callable)):
            buttonData = ButtonData(onClick=buttonData)

        return Button(
            op, rectData if isinstance(rectData, RectData) else RectData(*rectData),
            PanelData(
                text=text,
                toolTipText=ttt,
                canDrag=canDrag,
                toolTipImagePath=tti,
                parent=parent,
                rectIsLocal=rectIsLocal,
            ),
            buttonData,
            param=param
        )

    @staticmethod
    def checkBox(op: Boss_OT_base_ui,
                 rectData: rectDataType,
                 text: str = '',
                 value: bool = False,
                 onValueChange: callbackType = None,
                 ttt: str = '',
                 tti: str = '',
                 canDrag: bool = True,
                 parent: uiType = None,
                 rectIsLocal: bool = False,
                 param=None
                 ) -> CheckBox:
        return CheckBox(
            op,
            rectData if isinstance(rectData, RectData) else RectData(*rectData),
            PanelData(text,toolTipText=ttt,toolTipImagePath=tti,canDrag=canDrag,parent=parent,rectIsLocal=rectIsLocal),
            value=value, onValueChange=onValueChange, param=param
        )

    @staticmethod
    def textField(op: Boss_OT_base_ui,
                  rectData: rectDataType,
                  text: fieldType = '',
                  onValueChange: callbackType = None,
                  onTextChange: callbackType = None,
                  onEnterPress: callbackType = None,
                  ttt: str = '',
                  tti: str = '',
                  canDrag: bool = True,
                  parent: uiType = None,
                  rectIsLocal: bool = False,
                  param=None
                  ) -> TextField:

        return TextField(op, rectData if isinstance(rectData, RectData) else RectData(*rectData),
                         panelData=PanelData(text, toolTipText=ttt, toolTipImagePath=tti, canDrag=canDrag,
                                             parent=parent, rectIsLocal=rectIsLocal),
                         value=str(text),
                         onTextChange=onTextChange,
                         onValueChange=onValueChange,
                         onEnterPress=onEnterPress,
                         param=param
                         )

    @staticmethod
    def floatField(op: Boss_OT_base_ui,
                   rectData: rectDataType,
                   value: fieldType = None,
                   onValueChange: callbackType = None,
                   onTextChange: callbackType = None,
                   onEnterPress: callbackType = None,
                   ttt: str = '',
                   tti: str = '',
                   canDrag: bool = True,
                   parent: uiType = None,
                   rectIsLocal: bool = False,
                   param=None
                   ) -> FloatField:

        if isinstance(value, FieldValue):
            val = value.value
            minValue = value.min
            maxValue = value.max
            changeBy = value.changeBy if value.changeBy else .1
        else:
            val = value
            minValue = None
            maxValue = None
            changeBy = .1

        return FloatField(op, rectData if isinstance(rectData, RectData) else RectData(*rectData),
                          panelData=PanelData(toolTipText=ttt, toolTipImagePath=tti, canDrag=canDrag,
                                              parent=parent, rectIsLocal=rectIsLocal),
                          value=val,
                          minValue=minValue,
                          maxValue=maxValue,
                          changeBy=changeBy,
                          onTextChange=onTextChange,
                          onValueChange=onValueChange,
                          onEnterPress=onEnterPress,
                          param=param
                          )

    @staticmethod
    def intField(op: Boss_OT_base_ui,
                 rectData: rectDataType,
                 value: fieldType = None,
                 onValueChange: callbackType = None,
                 onTextChange: callbackType = None,
                 onEnterPress: callbackType = None,
                 ttt: str = '',
                 tti: str = '',
                 canDrag: bool = True,
                 parent: uiType = None,
                 rectIsLocal: bool = False,
                 param=None
                 ) -> IntField:

        if isinstance(value,FieldValue):
            val         = value.value
            minValue    = value.min
            maxValue    = value.max
            changeBy    = value.changeBy if value.changeBy else 1
        else:
            val      = value
            minValue = None
            maxValue = None
            changeBy = 1

        return IntField(op, rectData if isinstance(rectData, RectData) else RectData(*rectData),
                        panelData=PanelData(toolTipText=ttt, toolTipImagePath=tti, canDrag=canDrag,
                                            parent=parent, rectIsLocal=rectIsLocal),
                        value=val,
                        minValue=minValue,
                        maxValue=maxValue,
                        changeBy=changeBy,
                        onTextChange=onTextChange,
                        onValueChange=onValueChange,
                        onEnterPress=onEnterPress,
                        param=param
                        )
    @staticmethod
    def vectorIntField(op: Boss_OT_base_ui,
                       rectData: rectDataType,
                       value: vecFieldType = (0, 0, 0),
                       onValueChange: callbackType = None,
                       onTextChange: callbackType = None,
                       onEnterPress: callbackType = None,
                       ttt: str = '',
                       tti: str = '',
                       canDrag: bool = True,
                       parent: uiType = None,
                       rectIsLocal: bool = False,
                       param=None
                       ) -> VectorIntField:

        if isinstance(value, FieldValue):
            val         = value.value
            minValue    = value.min
            maxValue    = value.max
            changeBy    = value.changeBy if value.changeBy else (1, 1, 1)
        else:
            val      = value
            minValue = None
            maxValue = None
            changeBy = (1, 1, 1)

        return VectorIntField(op, rectData if isinstance(rectData, RectData) else RectData(*rectData),
                              bgPanelData=PanelData(toolTipText=ttt, toolTipImagePath=tti, canDrag=canDrag,
                                                  parent=parent, rectIsLocal=rectIsLocal),
                              value=val, minValue=minValue, maxValue=maxValue, changeBy=changeBy,
                              isHorizontal=True,
                              onTextChange=onTextChange,
                              onValueChange=onValueChange,
                              onEnterPress=onEnterPress,
                              param=param
                              )

    @staticmethod
    def vectorFloatField(op: Boss_OT_base_ui,
                         rectData: rectDataType,
                         value: vecFieldType = (.0, .0, .0),
                         onValueChange: callbackType = None,
                         onTextChange: callbackType = None,
                         onEnterPress: callbackType = None,
                         ttt: str = '',
                         tti: str = '',
                         canDrag: bool = True,
                         parent: uiType = None,
                         rectIsLocal: bool = False,
                         param=None
                         ) -> VectorFloatField:

        if isinstance(value, FieldValue):
            val = value.value
            minValue = value.min
            maxValue = value.max
            changeBy = value.changeBy if value.changeBy else (.1, .1, .1)
        else:
            val = value
            minValue = None
            maxValue = None
            changeBy = (.1, .1, .1)

        return VectorFloatField(op, rectData if isinstance(rectData, RectData) else RectData(*rectData),
                                bgPanelData=PanelData(toolTipText=ttt, toolTipImagePath=tti, canDrag=canDrag,
                                                    parent=parent, rectIsLocal=rectIsLocal),
                                value=val, minValue=minValue,maxValue=maxValue,changeBy=changeBy,
                                isHorizontal=True,
                                onTextChange=onTextChange,
                                onValueChange=onValueChange,
                                onEnterPress=onEnterPress,
                                param=param
                                )

    @staticmethod
    def vectorBooleanField(op: Boss_OT_base_ui,
                           rectData: rectDataType,
                           value: tuple = None,
                           onValueChange: callbackType = None,
                           ttt: str = '',
                           tti: str = '',
                           canDrag: bool = True,
                           parent: uiType = None,
                           rectIsLocal: bool = False,
                           param=None
                           ) -> VectorBooleanField:
        return VectorBooleanField(op, rectData if isinstance(rectData, RectData) else RectData(*rectData),
                                  bgPanelData=PanelData(toolTipText=ttt, toolTipImagePath=tti, canDrag=canDrag,
                                                      parent=parent, rectIsLocal=rectIsLocal),
                                  value=value, isHorizontal=True,
                                  onValueChange=onValueChange,
                                  param=param
                                  )

