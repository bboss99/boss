import bpy
from ..Geo.RectData import RectData
from ..Geo.RectGeo import (
    RectGeo,
    RoundRectGeo,
    RoundTopRectGeo,
    RoundBottomRectGeo,
)

from . Panel import Panel,PanelData
from ..  Text import TextData
from . Button import Button,ButtonData
from .. utils import clamp,_addCallback,json_loadPath,getStylesDict,loadStyle
from .. Color import Color
import blf
import re
from itertools import count,chain
from os.path import dirname,join

__all__ = ['TextField']

boss_dir = dirname(dirname(__file__))
op_settings_json_path = join(join(boss_dir,'settings'), 'op_settings.json')
op_settings = json_loadPath(op_settings_json_path)

draw_mode:str = op_settings['draw_mode']

del boss_dir
del op_settings_json_path
del op_settings

style = loadStyle(getStylesDict()['style_01'])

g_font_id = style.get('GlobalFontId', 0)
g_font_size = style.get('GlobalFontSize', 15)
g_font_color = style.get('GlobalFontColor', 15)
g_dpi = style.get('GlobalFontDpi', 72)

del style

class TextField():
    _ids = count(0)

    def __init__(   self,
                    op,
                    rectData,panelData=None,
                    value=None,onTextChange=None,onValueChange=None,onEnterPress = None,
                    active_color = None, param=None):
        self.op                 = op
        panelData               = panelData if panelData else PanelData() 

        if type(self) == TextField:
            panelData.panelType     = 'TextField'

        panelData.textData      = panelData.textData if panelData.textData else TextData.with_defaults()

        active_color            = active_color if active_color else op.uip.curStyle["TextFieldActiveColor"]  

        self.button             = Button(
                                        op,
                                        rectData,
                                        panelData,
                                        ButtonData(
                                            onClick=self._makeEditable
                                            )
                                        )
        
        self._setValue(value)  

        self.onTextChange       = []
        self.onValueChange      = []
        self.onEnterPress       = []

        if onTextChange:
            self.add_onTextChange(onTextChange)
        if onValueChange:
            self.add_onValueChange(onValueChange)
        if onEnterPress:
            self.add_onEnterPress(onEnterPress)
        
        self.param              = param

        self.normal_color       = panelData.normal_color    

        self.hover_color        = panelData.hover_color if panelData.hover_color else self.normal_color
        self.active_color       = active_color
        
        self.cursorHeight       = panelData.textData.fontSize
        
        self.cursorIndex        = len(self.text)

        self.text_field_id      = next(self._ids)  

        self.op.uip.add_textField(self)  

    def deleteUI(self):
        self.op.uip.remove_textField(self)
        self.button.deleteUI()

    def _getPrevSpaceIndex(self,pStr,pCursorIndex):
        text = pStr[:pCursorIndex]

        cursorShift = 0
        for i, ch in enumerate(reversed(text)):
            if ch == ' ':
                cursorShift = i+1

                for ch1 in reversed(text[:-cursorShift]):
                    if ch1 == ' ':
                        cursorShift += 1
                    else:
                        return cursorShift
        
        return pCursorIndex

    def _getNextSpaceIndex(self,pStr,pCursorIndex):        
        text = pStr[pCursorIndex:] 

        cursorShift = 0

        for i, ch in enumerate(text):
            if ch == ' ':
                cursorShift = i+1

                for ch1 in text[cursorShift:]:
                    if ch1 == ' ':
                        cursorShift += 1

                    else:
                        return cursorShift
        
        return len(pStr) - pCursorIndex
    
    def onKeyPress(self,keyid):
        if self.op.uip.ctrl_pressed and not self.op.uip.shift_pressed :
            if keyid == 'LEFT_ARROW':
                cursorShift = self._getPrevSpaceIndex(self.text, self.cursorIndex)                

                self._shiftCursorIndex(-cursorShift)
            
            elif keyid == 'RIGHT_ARROW':
                cursorShift = self._getNextSpaceIndex(self.text, self.cursorIndex)   

                self._shiftCursorIndex(cursorShift)

            elif keyid == 'BACK_SPACE':
                if len( self.text[:self.cursorIndex] ) > 0:                    
                    cursorShift = self._getPrevSpaceIndex(self.text, self.cursorIndex)                    

                    prev = self.text[:self.cursorIndex - cursorShift]
                    after = self.text[self.cursorIndex:]

                    self._setText(prev + after)
                    self._shiftCursorIndex(-cursorShift)
            
            elif keyid == 'DEL':
                if len( self.text[self.cursorIndex + 1:] ) > 0:
                    cursorShift = self._getNextSpaceIndex(self.text, self.cursorIndex)

                    prev    = self.text[:self.cursorIndex]
                    after   = self.text[self.cursorIndex + cursorShift:]
                    
                    self._setText( prev + after)
            
            elif keyid == 'V':
                clip = bpy.context.window_manager.clipboard
                
                if type(clip) is str:
                    self._setText( self.text[:self.cursorIndex] + clip + self.text[self.cursorIndex:] )
                self._shiftCursorIndex(len(clip))
            
            elif keyid == 'TAB':           
                self._moveToNextTextField(-1)
            
            elif keyid == 'X':
                pass
            elif keyid == 'C':
                pass
        
        elif self.op.uip.ctrl_pressed and self.op.uip.shift_pressed :
            pass
        
        elif not self.op.uip.ctrl_pressed and self.op.uip.shift_pressed :
            self._setText( self.text[:self.cursorIndex] + keyid + self.text[self.cursorIndex:] )
            self._shiftCursorIndex(1)
            pass
        else:            
            if keyid == 'BACK_SPACE':
                if len(self.text) > 0:
                    self._setText( self.text[:self.cursorIndex-1] + self.text[self.cursorIndex:] )
                    self._shiftCursorIndex(-1)                

            elif keyid == 'DEL':
                if len(self.text) > 0:
                    self._setText(self.text[:self.cursorIndex] + self.text[self.cursorIndex+1:] )

            elif keyid == 'RET':
                self._onEnterPress()

            elif keyid == 'LEFT_ARROW':
                self._shiftCursorIndex(-1)
            
            elif keyid == 'RIGHT_ARROW':           
                self._shiftCursorIndex(1)
            
            elif keyid == 'HOME':
                self._shiftCursorIndex(- len(self.text) )
            
            elif keyid == 'END':
                self._shiftCursorIndex( len(self.text) )
            
            elif keyid == 'TAB':
                self._moveToNextTextField(1)
            else:
                self._setText(self.text[:self.cursorIndex] + keyid + self.text[self.cursorIndex:])
                self._shiftCursorIndex(1)
        
        pass

    def _setText(self,text):
        if not self.text == text:
            self.text = text
            self._onTextChanged()

    def _onEnterPress(self):
        self._commitTextToValue(self.text)
        self._makeNonEditable()

        for each in self.onEnterPress:
            each()

    def _commitTextToValue(self,value):
        if value == self.value:
            pass
        else:
            self._setValue(value)
            for each in self.onValueChange:
                each()

    def _setValue(self,value):
        self.value  = '' if value == None else value
        self.text   = self.value
        self._changeTextGeo()

    def setValue(self, value):
        newValue = str(value)
        if newValue == self.value:
            pass
        else:
            self.value = newValue
            self._changeTextGeo()

    def _shiftCursorIndex(self,shiftBy=0):
        self.cursorIndex =  self.cursorIndex + shiftBy
        self.cursorIndex =  clamp(self.cursorIndex,0,len(self.text))

        if draw_mode != 'optimized':
            self._resetCursorPosition()
        else:
            self._resetCursorPositionG()

    def _resetCursorPositionG(self):
        blf.size(g_font_id, g_font_size, g_dpi)
        textWidth, textHeight = blf.dimensions(g_font_id, self.text[:self.cursorIndex])

        self.op.uip.cursor.setPositionAndSize(
            self.button._text.xPos + textWidth,
            self.button._text.yPos,
            self.cursorHeight * .2,
            self.cursorHeight
        )

    def _resetCursorPosition(self):
        blf.size(self.button._text.textData.font_id, self.button._text.textData.fontSize, g_dpi)
        textWidth, textHeight = blf.dimensions(self.button._text.textData.font_id, self.text[:self.cursorIndex])

        self.op.uip.cursor.setPositionAndSize(
            self.button._text.xPos + textWidth,
            self.button._text.yPos,
            self.cursorHeight*.2,
            self.cursorHeight
            )

    def _changeTextGeo(self):
        self.button._text.setText(self.text)
    
    def _onTextChanged(self):
        self._changeTextGeo()    

        for each in self.onTextChange:
            each()

    def _onEscapePressed(self):
        self.text = self._lastText
        self._setValue(self.text)
        self._makeNonEditable()

    def _makeNonEditable(self):
        self.op.uip.keyboardInput    = False
        self.op.uip.keyPress         = None
        self.button.geo.setColor(self.normal_color,'normal')

        self.endCursor()
        
    def _moveToNextTextField(self,moveBy):
        self._onEnterPress()        

        nextId = self.text_field_id + moveBy        

        for each in self.op.uip.ui_text_fields:
            if each.text_field_id == nextId:
                each._makeEditable(self)
                break

    def _makeEditable(self,*args):
        self._lastText                   = self.text
        self.op.uip.textFieldResetFunc   = self._onEscapePressed
        self.op.uip.keyPress             = self.onKeyPress
        self.op.uip.keyboardInput        = True        
        
        self.cursorIndex                = len(self.text) 
        
        self.op.uip.cursor.setPositionAndSize(
            self.button._text.xPos + self.button._text.textWidth,
            self.button._text.yPos,
            self.cursorHeight*.2,
            self.cursorHeight
            )
        
        self.op.uip._canDrawCursor          = True
        
        self.startCursor()
        self.button.geo.setColor(self.active_color, 'normal')

    def add_onTextChange(self,*params):
        _addCallback(self, self.onTextChange, *params)
           
    def add_onValueChange(self,*params):
        _addCallback(self,self.onValueChange,*params)
            
    def add_onEnterPress(self,*params):
        _addCallback(self,self.onEnterPress,*params)

    def startCursor(self):
        self.op.isCursorRunning  = True
        self.op._timer     = self.op.uip.context.window_manager.event_timer_add(1, window=self.op.uip.context.window)
    
    def endCursor(self):
        self.op.isCursorRunning    = False
        self.op.uip._canDrawCursor  = False
        self.op.uip.context.window_manager.event_timer_remove(self.op._timer)

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
        self.op.uip.add_textField(self) 
        
        for each in chain(self.getPanels(),self.getButtons()):
            each.enable(pCallbacks,pDrawable)

    def disable(self,pCallbacks=True,pDrawable = True):
        self.op.uip.remove_textField(self) 

        for each in chain(self.getPanels(),self.getButtons()):
            each.disable(pCallbacks,pDrawable)


