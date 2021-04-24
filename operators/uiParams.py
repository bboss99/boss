import bpy

from ..utils import (
    appendCheck,
    removeCheck,
    json_loadPath
)

from ..Geo.RectData import RectData
from ..ui.base_ui.PanelData import PanelData
from ..ui.Panel import Panel
from ..ui.Button import Button
from ..ui.TextField import TextField
from ..ui.ColorPicker import ColorPicker
from ..Color import Color

from enum import Enum

from ..Geo.Dims import DirectionLength

from typing import Union,List,Tuple,Callable,Dict,Optional
from os.path import dirname,join

uiListType = List[Union[Button, Panel]]
FnOrNone = Optional[Callable]

spaceTypesSet = {
    "CLIP_EDITOR",
    "CONSOLE",
    "DOPESHEET_EDITOR",
    "FILE_BROWSER",
    "GRAPH_EDITOR",
    "IMAGE_EDITOR",
    "INFO",
    "NLA_EDITOR",
    "NODE_EDITOR",
    "NODE_EDITOR_PATH",
    "OUTLINER",
    "PREFERENCES",
    "PROPERTIES",
    "SEQUENCE_EDITOR",
    "TEXT_EDITOR",
    "UV_EDITOR",
    "VIEW_3D",
}

class SpaceType(Enum):
    CLIP_EDITOR         = bpy.types.SpaceClipEditor
    CONSOLE             = bpy.types.SpaceConsole
    DOPESHEET_EDITOR    = bpy.types.SpaceDopeSheetEditor
    FILE_BROWSER        = bpy.types.SpaceFileBrowser
    GRAPH_EDITOR        = bpy.types.SpaceGraphEditor
    IMAGE_EDITOR        = bpy.types.SpaceImageEditor
    INFO                = bpy.types.SpaceInfo
    NLA_EDITOR          = bpy.types.SpaceNLA
    NODE_EDITOR         = bpy.types.SpaceNodeEditor
    NODE_EDITOR_PATH    = bpy.types.SpaceNodeEditorPath
    OUTLINER            = bpy.types.SpaceOutliner
    PREFERENCES         = bpy.types.SpacePreferences
    PROPERTIES          = bpy.types.SpaceProperties
    SEQUENCE_EDITOR     = bpy.types.SpaceSequenceEditor
    TEXT_EDITOR         = bpy.types.SpaceTextEditor
    UV_EDITOR           = bpy.types.SpaceUVEditor
    VIEW_3D             = bpy.types.SpaceView3D

    @staticmethod
    def from_str(spaceTypeStr):
        if spaceTypeStr in spaceTypesSet:
            return getattr(SpaceType, spaceTypeStr)
        else:
            return SpaceType.VIEW_3D

"""
class ClipNode():
    def __init__(self,clipRect,parentClipNode):
        self.clipRect           = clipRect
        self.uiElements         = []        

        self.parentClipNode     = parentClipNode
        self.childClipNodes     = []

class ClippingTree():
    def __init__(self):
        self.firstCN        = ClipNode(None,None)
        self.dict_cr_cn     = {} 

    def addUi(self,uiElement):
        if uiElement.clipRect == None:
            self.firstCN.uiElements.append(uiElement)

            return 

        if uiElement.clipRect in self.dict_cr_cn:
            clipNode = self.dict_cr_cn[uiElement.clipRect]
            
            clipNode.uiElements.append(uiElement)

        else:
            newClipNode = ClipNode(uiElement.clipRect,None)
            
            newClipNode.uiElements.append(uiElement)

            self.dict_cr_cn[uiElement.clipRect] = newClipNode

    def removeUi(self,uiElement):
        if uiElement.clipRect == None:
            self.firstCN.uiElements.remove(uiElement)
            return
        
        if uiElement.clipRect in self.dict_cr_cn:
            clipNode = self.dict_cr_cn[uiElement.clipRect]
            clipNode.uiElements.remove(uiElement)

    def removeUiSafe(self,uiElement):
        if uiElement.clipRect == None:
            if uiElement in self.firstCN.uiElements:
                self.firstCN.uiElements.remove(uiElement)
            return
        
        if uiElement.clipRect in self.dict_cr_cn:
            if uiElement.clipRect in self.dict_cr_cn:
                clipNode = self.dict_cr_cn[uiElement.clipRect]
                if uiElement in clipNode.uiElements:
                    clipNode.uiElements.remove(uiElement)
"""

boss_dir = dirname(dirname(__file__))
boss_settings_json_path = join(join(boss_dir, 'settings'), 'boss_settings.json')
boss_settings = json_loadPath(boss_settings_json_path)

del boss_dir
del boss_settings_json_path

class uiParams:
    def __init__(self,op):
        self.op = op

        self.dict_styles:   dict    = {}           
        self.curStyleName:  str     = 'style_01'    
        self.curStyle:      dict    = {}        

        self.dict_shader_geo: dict          

        self._batched                   = False

        self.gui_depth      : int   = 0

        self.use_hierarchy  :bool   = False

        self.dict_imgs      :dict   = {}  

        self.mouse_x:       int     = 0  
        self.mouse_y:       int     = 0  
        self.mouse_down_x:  int     = 0
        self.mouse_down_y:  int     = 0

        self._btnToDrag             = None
        self.region_width:  int     = 0  
        self.region_height: int     = 0  

        self.region_rect:   Union[RectData, None] = None  
        self.globalToolTip: Union[List[str], str] = None
        self.toolTipOffset: Tuple[int, int]       = boss_settings['ttt_offset']  

        self.toolTipAnchor          = 'MOUSE'

        self.toolTipAnchorCo        = (0, 0)
        self._globalToolTipPanel                    = None  
        self.globalToolTipImagePath: str            = ''  
        self.panelToolTipOffsets: Tuple[int, int]   = boss_settings['tti_offset']
        self.panelToolTipSize: Tuple[int, int]      = boss_settings['tti_size']

        self.panelToolTipAnchor     = 'MOUSE'

        self.panelToolTipAnchorCo     = (0, 0)

        self.panels:            List[Panel] = []

        self.all_gui:           uiListType  = []

        self.ui_drawable:       uiListType  = []
        self.ui_drawable_dirty: bool        = True
        self.ui_drawable_texts: uiListType  = []
        self.ui_drawable_texts_dirty: bool  = True

        self.ui_onClick:        uiListType  = []
        self.ui_onHover:        uiListType  = []

        self.ui_onMouseEnter:   uiListType  = []
        self.ui_onMouseExit:    uiListType  = []
        self.ui_onWheelUp:      uiListType  = []
        self.ui_onWheelDown:    uiListType  = []
        self.ui_onDragBegin:    uiListType  = []
        self.ui_onDrag:         uiListType  = []
        self.ui_onDragEnd:      uiListType  = []

        self.ui_mesh_parts:     Dict[ str, Union[Button, Panel]] = {}

        self.curLayout                  = None

        self._imgPath_imageData:    dict = {}
        self.list_imageData:        list = []
        self.list_imageData_unused: list = [] 

        self.keyboardInput:         bool                    = False
        self.keyPress:              FnOrNone                = None  
        self.shift_pressed:         bool                    = False
        self.ctrl_pressed:          bool                    = False
        self.alt_pressed:           bool                    = False
        self.textFieldResetFunc:    FnOrNone                = None

        self._canDrawCursor:bool    = False
        self._cursor = None

        self.text_field_id:         int             = 0
        self.ui_text_fields:        List[TextField] = []

        self.ui_lastCreated: Union[None,Panel,Button] = None  

        self._color_picker = None
        self.color_picker_fn:   FnOrNone        = None
        self.escapeFn:          List[Callable]  = []  

        self._last_disabled         = None

        self._last_draw_disabled    = []

        self.set_tt_anchor()

    def reset(self):
        pass

    def get_ttt_anchor_co(self):
        if self.toolTipAnchor == "MOUSE":
            return self.mouse_x, self.mouse_y
        return self.toolTipAnchorCo

    def get_tti_anchor_co(self):
        if self.panelToolTipAnchor == "MOUSE":
            return self.mouse_x,self.mouse_y
        return self.panelToolTipAnchorCo

    def set_tt_anchor(self):
        if self.toolTipAnchor == "MOUSE":
            pass
        else:
            if self.toolTipAnchor == "BL":
                self.toolTipAnchorCo = (self.region_rect.xMin,self.region_rect.yMin)
            elif self.toolTipAnchor == "TL":
                self.toolTipAnchorCo = (self.region_rect.xMin,self.region_rect.yMax)
            elif self.toolTipAnchor == "TR":
                self.toolTipAnchorCo = (self.region_rect.xMax,self.region_rect.yMax)
            elif self.toolTipAnchor == "BR":
                self.toolTipAnchorCo = (self.region_rect.xMax,self.region_rect.yMin)
        if self.panelToolTipAnchor == "MOUSE":
            if self.panelToolTipAnchor == "BL":
                self.panelToolTipAnchorCo = (self.region_rect.xMin,self.region_rect.yMin)
            elif self.panelToolTipAnchor == "TL":
                self.panelToolTipAnchorCo = (self.region_rect.xMin,self.region_rect.yMax)
            elif self.panelToolTipAnchor == "TR":
                self.panelToolTipAnchorCo = (self.region_rect.xMax,self.region_rect.yMax)
            elif self.panelToolTipAnchor == "BR":
                self.panelToolTipAnchorCo = (self.region_rect.xMax,self.region_rect.yMin)

    @property
    def cursor(self):
        if self._cursor:
            return self._cursor
        else:
            self._cursor = Panel(
                self.op,
                RectData(0, 0, 15, 15),
                PanelData(
                    normal_color=Color.GRAY_P04,
                    canDrag=False,
                    addToUI=False,
                    name='uip.cursor'
                )
            )
            return self._cursor

    @property
    def globalToolTipPanel(self):
        if self._globalToolTipPanel:
            return self._globalToolTipPanel
        else:
            self._globalToolTipPanel = Panel(
                self.op,
                RectData(
                    self.mouse_x + self.panelToolTipOffsets[0],
                    self.mouse_y + self.panelToolTipOffsets[1],
                    self.panelToolTipSize[0],
                    self.panelToolTipSize[1]
                ),
                PanelData(
                    image_path=self.dict_imgs['default.png'],
                    normal_color=(1, 1, 1, 1),
                    canDrag=False,
                    addToUI=False,
                    name='uip.globalToolTipPanel'
                )
            )
            return self._globalToolTipPanel

    @property
    def color_picker(self):
        if self._color_picker:
            return self._color_picker
        else:
            self._color_picker = ColorPicker(self.op, 300, Color.WHITE, 8)
            self._color_picker.setEnabledState(False)  
            return self._color_picker

    def add_textField(self,tf):
        appendCheck(self.ui_text_fields,tf)
        
    def remove_textField(self,tf):
        removeCheck(self.ui_text_fields,tf)

    def getNextGuiDepth(self):
        self.gui_depth +=1
        return self.gui_depth

    def deleteAllUi(self):
        allgui = [each for each in self.all_gui]
        for a in allgui:
            a.deleteUI()

    def disableUi(self,ui_list:Union[List,None] = None):
        self._last_disabled = ui_list if ui_list else self.all_gui.copy()

        for a in self._last_disabled:
            a.disable(True, False)

        disCol = self.curStyle['DisabledColor']
        for a in self.ui_drawable:
            if a.geo:
                a.geo.setVertexColor(disCol)
                self._last_draw_disabled.append(a)

    def enableUi(self):
        for a in self._last_disabled:
            a.enable()
        for a in self._last_draw_disabled:
            a.geo.setVertexColor(a.geo.normal_colors)

    def deleteImageFiles(self):
        allImgs = bpy.data.images

        for i in self.list_imageData:
            allImgs.remove(i, do_unlink=True)

        for i in self.list_imageData_unused:
            allImgs.remove(i, do_unlink=True)
    
    def loadFile(self,img_path):
        if img_path in self._imgPath_imageData:
            return self._imgPath_imageData[img_path]
        else:
            if len(self.list_imageData_unused) > 0:
                imgData = self.list_imageData_unused.pop(0)
                imgData.filepath = img_path

            else:
                imgData = bpy.data.images.load(img_path, check_existing=False)

            self.list_imageData.append(imgData)

            self._imgPath_imageData[img_path] = imgData
            if imgData.gl_load():
                raise Exception()
            return imgData

    def addCombinedMesh(self,ui_element:Union[Panel,Button]):
        mesh_part = ui_element.mesh_part
        p: Panel  
        if mesh_part not in self.ui_mesh_parts:
            p = Panel(
                self.op,
                RectData(),
                PanelData(geo_type='CM',image_path=ui_element.geo.geoData.image_path)
            )
            self.ui_mesh_parts[mesh_part] = p 
            p.rectData.remove_onUpdate(p.geo.updateVerts)
        else:
            p = self.ui_mesh_parts[mesh_part]

        ui_element.rectData.add_onUpdate(p.geo.updateVerts, ui_element)

        self.ui_mesh_parts[mesh_part].geo.add_geometry(ui_element)

        return p

    def getEmptySpaceAroundPoint(self,ptx,pty):
        return DirectionLength(
            ptx - self.region_rect.xMin,
            self.region_rect.xMax - ptx,
            pty - self.region_rect.yMin,
            self.region_rect.yMax - pty
        )

    def getEmptySpaceAroundRect(self,rectData:RectData):
        return DirectionLength(
            rectData.xMin - self.region_rect.xMin,
            self.region_rect.xMax - rectData.xMax,
            rectData.yMin - self.region_rect.yMin,
            self.region_rect.yMax - rectData.yMax
        )
