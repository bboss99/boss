from ..Geo.base_geo.GeoData import GeoData
from ..Geo.RectData import RectData

from ..Geo.RectGeo import (
    RectGeoData,
    RectGeo,
    RoundRectGeo,
    RRGeoData,
    RoundTopRectGeo,
    RRTGeoData,
    RoundBottomRectGeo,
    RRBGeoData,
)

from ..Geo.CombinedMesh import CombinedMeshGeo
from .. Geo.EllipseGeo import EllipseGeo, EllipseGeoData
from .. Text import Text, TextData
from .. utils import appendCheck, removeCheck
from . base_ui.PanelData import PanelData
from pprint import pformat
from itertools import count

__all__ = ['Panel']

class Panel:
    _ids = count(0)

    def __str__(self):
        return self.name

    def __init__(self, op, rectData, panelData=None, param=None):
        self.op                 = op
        panelData               = PanelData.apply_style(panelData, op.uip.curStyle)
        self.param              = param  
        self.name               = 'panel_' + str(next(self._ids)) if panelData.name == '' else panelData.name

        self.clipRect:RectData  = panelData.clipRect  

        if self.clipRect:
            self.clipRect._set_clip_min_max()
            self.clipRect.add_onUpdate(self.clipRect._set_clip_min_max)  

        self._partOf            = {}
        self.enabled            = True
        self.mesh_part          = panelData.mesh_part
        self.mesh_part_ui       = None

        if not rectData:
            self.layout         = self.op.uip.curLayout
            self.rectData:RectData= self.layout.getNextRectData(self)
        else:
            self.rectData:RectData= rectData
            self.layout         = None

        self._canDraw           = True

        self.geo                = None
        self.setGeoFromPanelData(panelData)

        if self.geo:
            self._setImage()

            if self.mesh_part:
                self.rectData.add_onUpdate(self.geo.updateVerts)
            else:
                self.rectData.add_onUpdate(self.geo.updateVerts)

        self._text              = self.createText_fromTextData(panelData.textData, panelData.text)

        if self._text:
            self.rectData.add_onUpdate(self._text.setTextPosition)

            if panelData.resizeToText:
                self.setRectToText(panelData.resizeToText)

        self.gui_depth          = self.op.uip.getNextGuiDepth()

        self.children           = []

        self._deepChildrenSet   = False
        self.deepChildren       = []

        self.toolTipText        = panelData.toolTipText

        self.parent             = None  

        self.setParent(panelData.parent, not panelData.rectIsLocal)

        self.toolTipImagePath   = panelData.toolTipImagePath
        self.canDrag            = panelData.canDrag  

        self.dragRect = None
        self.setDragRect(panelData.dragRect)

        self._isMouseInside     = False  

        self._setDrawFunc()

        if panelData.addToUI:
            self.appendUI()
            if panelData.after_create_fn:
                panelData.after_create_fn(self)

    def setRectToText(self, resizeToText):
        if type(resizeToText) is tuple:
            self.rectData.setPositionAndSize(
                self.rectData.xMin,
                self.rectData.yMin,
                self._text.textWidth + resizeToText[0] * 2,
                self.rectData.height
            )
        else:
            self.rectData.setPositionAndSize(
                self.rectData.xMin,
                self.rectData.yMin,
                self._text.textWidth,
                self.rectData.height
            )
        self._text.setTextPosition()

    def _setDrawFunc(self):
        if self.mesh_part:
            if self._text:
                self.draw = self._drawOnlyText
        else:
            if self.geo and self._text:
                self.draw = self._draw
            elif self.geo:
                self.draw = self._drawOnlyGeo
            elif self._text:
                self.draw = self._drawOnlyText
            else:
                print(f'not drawing anything - {self.name}, will not be drawing')
                self.draw = self._drawNothing
                self.canDraw = False  

    def updateGeo_fromGeoType(self, geo_type):
        gd              = self.geo.geoData
        normal_color    = gd.normal_color
        hover_color     = gd.hover_color
        image_path      = gd.image_path

        self.rectData.remove_onUpdate(self.geo.updateVerts)

        self.geo        = self.createGeo_fromGeoData(
            createGeoDataFromGeoType(
                geo_type,
                normal_color,
                hover_color,
                image_path
            )
        )

        self.rectData.add_onUpdate(self.geo.updateVerts)

    def createText_fromTextData(self, textData, text):
        if textData:
            return Text(
                        text,
                        self.rectData,
                        textData,
                        self.clipRect
                    )
        return None

    def setGeoFromPanelData(self, panelData:PanelData):
        geo_type = panelData.geo_type

        if type(geo_type) is str:
            self.setGeoFromGeoType(geo_type,panelData.normal_color,panelData.hover_color,panelData.image_path)
        elif isinstance(panelData.geo_type,GeoData):
            geo_type.image_path = geo_type.image_path if geo_type.image_path else panelData.image_path

            self.setGeoFromGeoData(geo_type)
        else:
            pass

    def setGeoFromGeoType(self,geo_type:str,normal_color,hover_color,image_path):
        if geo_type == 'Rect':
            self.geo = RectGeo(
                self.rectData,
                self.clipRect,
                RectGeoData(
                    geo_type,
                    normal_color,
                    hover_color,
                    image_path
                )
            )
        elif geo_type == 'RR':
            self.geo = RoundRectGeo(
                self.rectData,
                self.clipRect,
                RRGeoData(
                    geo_type,
                    normal_color,
                    hover_color,
                    self.op.uip.dict_imgs['Circle32.png']
                )
            )
        elif geo_type == 'RRT':
            self.geo = RoundTopRectGeo(
                self.rectData,
                self.clipRect,
                RRTGeoData(
                    geo_type,
                    normal_color,
                    hover_color,
                    image_path
                )
            )
        elif geo_type == 'RRB':
            self.geo = RoundBottomRectGeo(
                self.rectData,
                self.clipRect,
                RRBGeoData(
                    geo_type,
                    normal_color,
                    hover_color,
                    image_path
                )
            )
        elif geo_type == 'CM':
            self.geo = CombinedMeshGeo(
                self.rectData,
                self.clipRect,
                GeoData(
                    geo_type,
                    normal_color,
                    hover_color,
                    image_path
                )
            )
        elif geo_type == 'CIR':
            self.geo = EllipseGeo(
                self.rectData,
                self.clipRect,
                EllipseGeoData(
                    geo_type,
                    normal_color,
                    hover_color,
                    image_path
                )
            )

    def setGeoFromGeoData(self, geoData):
        T = RectGeo
        if isinstance(geoData, RectGeoData):
            pass
        elif isinstance(geoData,RRGeoData):
            T = RoundRectGeo
        elif isinstance(geoData,RRTGeoData):
            T = RoundTopRectGeo
        elif isinstance(geoData,RRBGeoData):
            T = RoundBottomRectGeo
        elif isinstance(geoData, EllipseGeoData):
            T = EllipseGeo

        self.geo = T(self.rectData, self.clipRect, geoData)

    def setDragRect(self, dragRect):
        self.dragRect = dragRect if dragRect else self.op.uip.region_rect
        self._setAvailableSpace()  

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
        uip.panels.append(self)
        uip.all_gui.append(self)

    @property
    def text(self):
        return self._text.text

    @property
    def canDraw(self):
        return self._canDraw

    @canDraw.setter
    def canDraw(self, value):
        self._canDraw = value
        if self._canDraw:
            if self.mesh_part:
                self.mesh_part_ui.geo.add_geometry(self)
            else:
                if self.geo:
                    if appendCheck(self.op.uip.ui_drawable, self):
                        self.op.uip.ui_drawable_dirty = True
                if self._text:
                    if appendCheck(self.op.uip.ui_drawable_texts, self):
                        self.op.uip.ui_drawable_texts_dirty = True

        else:
            if self.mesh_part:
                self.mesh_part_ui.geo.remove_geometry(self)
            else:
                if self.geo:
                    if removeCheck(self.op.uip.ui_drawable, self):
                        self.op.uip.ui_drawable_dirty = True
                if self._text:
                    if removeCheck(self.op.uip.ui_drawable_texts, self):
                        self.op.uip.ui_drawable_texts_dirty = True

    def _falsifyDeepChildrenSet(self):
        curParent = self
        while curParent:
            curParent._deepChildrenSet = False
            curParent = curParent.parent

    def guiDepth_bringToFront(self):
        self.gui_depth = self.op.uip.getNextGuiDepth()

    def alignToParent(self):
        self.setPosition(self.parent.rectData.xMin + self.rectData.xMin, self.parent.rectData.yMin + self.rectData.yMin)

    def getChildren(self, deep=False):
        if not deep:
            return self.children
        else:
            if self._deepChildrenSet:
                return self.deepChildren
            else:
                deepChildren = []
                toCheck = []
                deepChildren.extend(self.children)
                toCheck.extend(self.children)

                safeCnt = 0

                while len(toCheck) > 0 and safeCnt < 50:
                    safeCnt += 1
                    deepChildren.extend(toCheck[0].children)
                    toCheck.extend(toCheck[0].children)
                    toCheck.pop(0)  

                self.deepChildren = deepChildren
                self._deepChildrenSet = True

                return self.deepChildren

    def _clearParent(self, keepWorldLocation=True):
        if not self.parent:
            return False

        if removeCheck(self.parent.children, self):
            if not keepWorldLocation:
                self.rectData.setPosition(
                    self.rectData.xMin - self.parent.rectData.xMin,
                    self.rectData.yMin - self.parent.rectData.yMin
                )
            self.parent = None
            return True

        return False

    def setParent(self, parent, keepWorldLocation=True):
        if not parent:
            if self._clearParent(keepWorldLocation):
                self._falsifyDeepChildrenSet()
            return

        if self.parent:
            if parent == self.parent:
                print("this is already parent. no change.")
                return
            else:
                if self._clearParent(keepWorldLocation):
                    self.parent = parent
                    appendCheck(self.parent.children, self)

                    self._falsifyDeepChildrenSet()

                    if not keepWorldLocation:
                        self.alignToParent()
        else:
            self.parent = parent
            appendCheck(self.parent.children, self)

            self._falsifyDeepChildrenSet()

            if not keepWorldLocation:
                self.alignToParent()

    def setEnabledState(self, enableState = True, pCallbacks=True, pDrawable = True):
        if enableState:
            self.enable(pCallbacks, pDrawable)
        else:
            self.disable(pCallbacks, pDrawable)

    def enable(self, pCallbacks=True, pDrawable = True):
        self.enabled = True
        if pCallbacks:
            for key, listValue in self._partOf.items():
                appendCheck(listValue, self)
        if pDrawable:
            self.canDraw = True

    def disable(self, pCallbacks=True, pDrawable = True):
        self.enabled = False

        if pCallbacks:
            for key, listValue in self._partOf.items():
                removeCheck(listValue, self)

        if pDrawable:
            self.canDraw = False

    def testInfo(self):
        print(f"name - {self.name} , parent - {self.parent}, parent's dad - {self.parent.parent}")

    def deleteUI(self, deleteChildren=False, deepChildren = True):
        if deleteChildren:
            for ui in self.getChildren(deepChildren):
                ui.deleteUI(True)  

        self.disable(pCallbacks=True, pDrawable = True)

        self._partOf = {}  

        if self.layout:
            self.layout.ui_elements.remove(self)
            self.layout = None

        removeCheck(self.op.uip.all_gui, self)

        self.setParent(None)

        if not deleteChildren:
            for child in self.children:
                child.setParent(None)

    def setClipRect(self, clipRect):
        self.clipRect = clipRect
        self.clipRect._set_clip_min_max()

        if self.geo:
            self.geo.setClipRect(clipRect)
        self._text.setClipRect(clipRect)

    def _drawOnlyText(self):
        self._text.draw()
        pass

    def _drawNothing(self):
        print(f'drawing nothing, neither geo nor text - {self}')
        pass

    def _drawOnlyGeo(self):
        self.geo.draw()

    def _draw(self):
        self.geo.draw()
        self._text.draw()

    def shiftPanelPosition(self, dx, dy):
        cdx, cdy = self._getConstrainedMovement(dx, dy)

        self.setPosition(self.rectData.xMin + cdx, self.rectData.yMin + cdy)

        self._setAvailableSpace()  

        for child in self.getChildren(deep=True):
            child.setPosition(child.xMin + cdx, child.yMin + cdy)

    def setPositionWithChildren(self, x, y):
        dx = x - self.xMin
        dy = y - self.yMin

        self.setPosition(x, y)

        for child in self.getChildren(deep=True):
            child.setPosition(child.xMin + dx, child.yMin + dy)

    def _getConstrainedMovement(self, dx, dy):
        if dx < 0:
            cdx = max(dx, self.avlLeft)  
        else:
            cdx = min(dx, self.avlRight)

        if dy < 0:
            cdy = max(dy, self.avlBottom)  
        else:
            cdy = min(dy, self.avlTop)

        return cdx, cdy

    def _setAvailableSpace(self):
        self.avlRight    = self.dragRect.xMax - self.rectData.xMax      

        self.avlLeft     = self.dragRect.xMin - self.rectData.xMin      

        self.avlTop      = self.dragRect.yMax - self.rectData.yMax      

        self.avlBottom   = self.dragRect.yMin - self.rectData.yMin      

    def setPositionAndSize_fromRectData_Local(self, rectData):
        if self.geo:
            self.geo._batched = False
        self.setPositionAndSize_Local(
                                rectData.xMin,
                                rectData.yMin,
                                rectData.width,
                                rectData.height,
                                )

    def setPositionAndSize_Local(self, xMin, yMin, width, height):
        if self.parent:
            if self.geo:
                self.geo._batched = False
            self.rectData.setPositionAndSize(
                self.parent.rectData.xMin + xMin,
                self.parent.rectData.yMin + yMin,
                width,
                height
            )
        else:
            if self.geo:
                self.geo._batched = False
            self.rectData.setPositionAndSize(
                xMin,
                yMin,
                width,
                height
            )

    def setPosition_Local(self, xMin, yMin):
        if self.parent:
            if self.geo:
                self.geo._batched = False
            self.rectData.setPosition(
                self.parent.rectData.xMin + xMin,
                self.parent.rectData.yMin + yMin,
            )

    def getRectData(self):
        return self.rectData

    def setPosition(self, x, y):
        if self.geo:
            self.geo._batched = False
        self.rectData.setPosition(x, y)

    def setPositionAndSize(self, xMin, yMin, width, height):
        if self.geo:
            self.geo._batched = False
        self.rectData.setPositionAndSize(
            xMin,
            yMin,
            width,
            height
        )

    def setPositionAndSize_minMax(self, xMin, yMin, xMax, yMax):
        if self.geo:
            self.geo._batched = False
        self.rectData.setPositionAndSize_minMax(
            xMin,
            yMin,
            xMax,
            yMax
        )

    def setPositionAndSize_fromRectData(self, rectData):
        if self.geo:
            self.geo._batched = False
        self.rectData.setPositionAndSize_fromRectData(rectData)

    def getLastCreatedUI(self):
        return self

    def _onDragBegin(self):
        self._old_xMin = self.rectData.xMin
        self._old_yMin = self.rectData.yMin

        if self.canDrag:
            self._setAvailableSpace()

            for child in self.getChildren(deep=True):
                child._onDragBegin()

        pass

    def reloadImagePath(self, image_path):
        self.geo.geoData.image_path = image_path
        self._setImage()

    def _setImage(self):
        if self.geo.geoData.image_path == '':
            imageData = None
        else:
            imageData  = self.op.uip.loadFile(self.geo.geoData.image_path)

        self._onImageSet(imageData)

    def _onImageSet(self,imageData):
        self.geo._batched = False  
        self.geo.imageData = imageData

    @property
    def xMin(self):
        return self.rectData.xMin

    @property
    def yMin(self):
        return self.rectData.yMin

    @property
    def xMax(self):
        return self.rectData.xMax

    @property
    def yMax(self):
        return self.rectData.yMax

    @property
    def width(self):
        return self.rectData.width

    @property
    def height(self):
        return self.rectData.height

    @property
    def getRight(self):
        return self.rectData.getRight

    @property
    def getLeft(self):
        return self.rectData.getLeft

    @property
    def getTop(self):
        return self.rectData.getTop

    @property
    def getBottom(self):
        return self.rectData.getBottom


