from . Panel import Panel, PanelData
from .. utils import    (
                            appendCheck,
                            removeCheck,
                            _addCallback
                        )   
from typing import Union,Callable,Tuple
__all__ = ['Button','ButtonData']

class ButtonData():
    def __init__(   self,
                    onClick = None,
                    onHover =None,
                    onMouseEnter =None,
                    onMouseExit =None,
                    onWheelUp =None,
                    onWheelDown =None,
                    onDragBegin =None,
                    onDrag =None,
                    onDragEnd =None,
                ):        
        self.onClick        = onClick     
        self.onHover        = onHover     
        self.onMouseEnter   = onMouseEnter
        self.onMouseExit    = onMouseExit 
        self.onWheelUp      = onWheelUp   
        self.onWheelDown    = onWheelDown 
        self.onDragBegin    = onDragBegin 
        self.onDrag         = onDrag      
        self.onDragEnd      = onDragEnd   

    def getList(self):
        return(
            self.onClick,
            self.onHover,
            self.onMouseEnter,
            self.onMouseExit,
            self.onWheelUp,
            self.onWheelDown,
            self.onDragBegin,
            self.onDrag,
            self.onDragEnd
        )

class Button(Panel):
    def __init__(self, op, rectData, panelData=None, buttonData=None, param=None):
        if panelData:
            if panelData.panelType == '':
                panelData.panelType = 'Button'
        else:
            panelData = PanelData()
            panelData.panelType = 'Button'

        panelData.addToUI           = False  
        
        Panel.__init__(self, op, rectData, panelData)

        self.param                  = param 

        self.onClick, self.onHover          = [],[]

        self.onMouseEnter, self.onMouseExit = [],[]

        self.onWheelUp, self.onWheelDown    = [], []

        self.onDragBegin, self.onDrag, self.onDragEnd = [], [], []

        if buttonData:
            self.add_onClick        (buttonData.onClick)

            self.add_onHover        (buttonData.onHover)

            self.add_onMouseEnter   (buttonData.onMouseEnter)
            self.add_onMouseExit    (buttonData.onMouseExit)

            self.add_onWheelUp      (buttonData.onWheelUp)
            self.add_onWheelDown    (buttonData.onWheelDown)

            self.add_onDragBegin    (buttonData.onDragBegin)
            self.add_onDrag         (buttonData.onDrag)
            self.add_onDragEnd      (buttonData.onDragEnd)

        if self.geo:
            if self.geo.hover_colors:
                self.add_onMouseEnter(self._changeColor, True)
                self.add_onMouseExit (self._changeColor, False)
            else:
                if appendCheck(self.op.uip.ui_onMouseEnter, self):
                    self._partOf['ui_onMouseEnter'] = self.op.uip.ui_onMouseEnter
                pass

        self.appendUI()

        if panelData.after_create_fn:
            panelData.after_create_fn(self)

    def appendUI(self):
        uip = self.op.uip

        if self._canDraw:
            if self.mesh_part:
                self.mesh_part_ui = uip.addCombinedMesh(self)
            else:
                if self.geo:
                    uip.ui_drawable.append(self)
                    uip.ui_drawable_dirty = True
                if self._text:
                    uip.ui_drawable_texts.append(self)
                    uip.ui_drawable_texts_dirty = True

        uip.ui_lastCreated = self
        uip.all_gui.append(self)

        if self.canDrag:
            if appendCheck(uip.ui_onDragBegin, self):
                self._partOf['ui_onDragBegin'] = uip.ui_onDragBegin

    def add_onClick(self, *params):
        if _addCallback(self, self.onClick, *params):
            appendCheck(self.op.uip.ui_onClick, self)
            self._partOf['ui_onClick'] = self.op.uip.ui_onClick

    def _removeCallBack(self, func, callBackList, globalUIList, partOfKey):
        for oc in callBackList:
            if oc.func == func:
                callBackList.remove(oc)
                break
        
        if not callBackList:
            removeCheck(globalUIList, self)
            self._partOf.pop(partOfKey, None)

    def remove_onClick(self, func):
        self._removeCallBack(func, self.onClick, self.op.uip.ui_onClick, 'ui_onClick')

    def add_onHover(self, *params):
        if _addCallback(self, self.onHover, *params):
            appendCheck(self.op.uip.ui_onHover, self)
            self._partOf['ui_onHover'] = self.op.uip.ui_onHover
   
    def remove_onHover(self, func):
        self._removeCallBack(func, self.onHover, self.op.uip.ui_onHover, 'ui_onHover' )

    def add_onMouseEnter(self, *params):
        if _addCallback(self, self.onMouseEnter, *params):
            appendCheck(self.op.uip.ui_onMouseEnter, self)
            self._partOf['ui_onMouseEnter'] = self.op.uip.ui_onMouseEnter

    def remove_onMouseEnter(self,func):
        self._removeCallBack(func, self.onMouseEnter, self.op.uip.ui_onMouseEnter, 'ui_onMouseEnter' )

    def add_onMouseExit(self, *params):
        if _addCallback(self, self.onMouseExit, *params):
            appendCheck(self.op.uip.ui_onMouseExit, self)
            self._partOf['ui_onMouseExit'] = self.op.uip.ui_onMouseExit  
    
    def remove_onMouseExit(self, func):
        self._removeCallBack(func, self.onMouseExit, self.op.uip.ui_onMouseExit, 'ui_onMouseExit' )

    def add_onWheelUp(self, *params):
        if _addCallback(self, self.onWheelUp, *params):
            appendCheck(self.op.uip.ui_onWheelUp, self)
            self._partOf['ui_onWheelUp'] = self.op.uip.ui_onWheelUp
    
    def remove_onWheelUp(self, func):
        self._removeCallBack(func, self.onWheelUp, self.op.uip.ui_onWheelUp, 'ui_onWheelUp')

    def add_onWheelDown(self, *params):
        if _addCallback(self, self.onWheelDown, *params):
            appendCheck(self.op.uip.ui_onWheelDown, self)
            self._partOf['ui_onWheelDown'] = self.op.uip.ui_onWheelDown  
    
    def remove_onWheelDown(self, func):
        self._removeCallBack(func, self.onWheelDown, self.op.uip.ui_onWheelDown, 'ui_onWheelDown')

    def add_onDragBegin(self, *params):
        if _addCallback(self, self.onDragBegin, *params):
            appendCheck(self.op.uip.ui_onDragBegin, self)
            self._partOf['ui_onDragBegin'] = self.op.uip.ui_onDragBegin

    def remove_onDragBegin(self, func):
        self._removeCallBack(func, self.onDragBegin, self.op.uip.ui_onDragBegin, 'ui_onDragBegin')

    def add_onDrag(self, *params):
        if _addCallback(self, self.onDrag,*params):
            appendCheck(self.op.uip.ui_onDrag, self)
            self._partOf['ui_onDrag'] = self.op.uip.ui_onDrag

    def remove_onDrag(self, func):
        self._removeCallBack(func, self.onDrag, self.op.uip.ui_onDrag, 'ui_onDrag' )

    def add_onDragEnd(self, *params):
        if _addCallback(self, self.onDragEnd,*params):
            appendCheck(self.op.uip.ui_onDragEnd, self)
            self._partOf['ui_onDragEnd'] = self.op.uip.ui_onDragEnd

    def remove_onDragEnd(self, func):
        self._removeCallBack(func, self.onDragEnd, self.op.uip.ui_onDragEnd, 'ui_onDragEnd')

    def _onClick(self):
        for each in self.onClick:
            each()

    def _onHover(self):
        for each in self.onHover:
            each()

    def _onWheelUp(self):
        for fn in self.onWheelUp:
            fn()

    def _onWheelUp_hierarchy(self, mouse_x, mouse_y):
        for fn in self.onWheelUp:
            fn()

        for ui in self.children:
            ui._onWheelUp_hierarchy(mouse_x, mouse_y)

    def _onWheelDown(self):
        for fn in self.onWheelDown:
            fn()

    def _onWheelDown_hierarchy(self, mouse_x, mouse_y):
        for fn in self.onWheelDown:
            fn()

        for ui in self.children:
            ui._onWheelDown_hierarchy(mouse_x, mouse_y)

    def _changeColor(self, mouseEntered):
        if self.canDraw:
            if self.mesh_part:
                self.mesh_part_ui.geo._changeColor(self, mouseEntered)
            else:
                if mouseEntered:
                    self.geo.setVertexColor(self.geo.hover_colors)
                else:
                    self.geo.setVertexColor(self.geo.normal_colors)

    def _onMouseEnter(self):
        self.op.uip.globalToolTip = self.toolTipText(self) if callable(self.toolTipText) else self.toolTipText

        if not self.toolTipImagePath == '':
            img_path = self.toolTipImagePath(self) if callable(self.toolTipImagePath) else self.toolTipImagePath
            self.op.uip.globalToolTipImagePath = img_path
            self.op.uip.globalToolTipPanel.reloadImagePath(img_path)

        for each in self.onMouseEnter:
            each()

    def _onMouseExit(self):
        self.op.uip.globalToolTip = None

        self.op.uip.globalToolTipImagePath = ''

        for each in self.onMouseExit:
            each()

    def _onDragBegin(self):
        self._old_xMin = self.rectData.xMin
        self._old_yMin = self.rectData.yMin

        if self.canDrag:
            self._setAvailableSpace()
            
            for child in self.getChildren(deep=True):
                child._onDragBegin()
        
        for fn in self.onDragBegin:
            fn()

    def _onDrag(self, dx, dy):
        if not self.canDrag:
            return

        for fn in self.onDrag:
            fn()

        cdx, cdy = self._getConstrainedMovement(dx, dy)

        self.setPosition(self._old_xMin + cdx, self._old_yMin + cdy)

        for child in self.getChildren(deep=True):
            child.setPosition(child._old_xMin + cdx, child._old_yMin + cdy)

    def _onDragEnd(self):
        for fn in self.onDragEnd:
            fn()

    def check_mouse_enter_exit(self, mouse_x, mouse_y):
        newIsMouseInside = self.rectData.isPointInside(mouse_x, mouse_y)

        if self._isMouseInside:
            if newIsMouseInside:
                pass
            else:
                self._isMouseInside = False
                self._onMouseExit()
        else:
            if newIsMouseInside:
                self._isMouseInside = True
                self._onMouseEnter()
            else:
                pass

    def check_mouse_enter_exit_hierarchy(self, mouse_x, mouse_y):
        newIsMouseInside = self.rectData.isPointInside(mouse_x, mouse_y)

        if self._isMouseInside:
            if newIsMouseInside:
                pass
            else:
                self._isMouseInside = False
                self._onMouseExit()
        else:
            if newIsMouseInside:
                self._isMouseInside = True
                self._onMouseEnter()
            else:
                pass

        for ui in self.children:
            ui.check_mouse_enter_exit_hierarchy(mouse_x, mouse_y)


