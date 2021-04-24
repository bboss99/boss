import bpy

from ..Geo.RectData import RectData

from ..utils import (
    getShaderDict,
    getStylesDict,
    get_dict_imageName_imagePath,
    loadStyle,
    json_loadPath
)
from typing import List,Union
from .uiParams import uiParams, SpaceType, spaceTypesSet
from . import TextFieldInput
from . import NormalInput

import time
import traceback
from ..ui.Panel import Panel
from ..ui.base_ui.PanelData import PanelData
from .op_utils import HudText, msgType
from pprint import pprint
from os.path import dirname,join

__all__ = ['Boss_OT_base_ui']
from . import drawing_callbacks

draw_mode:str

boss_dir = dirname(dirname(__file__))
op_settings_json_path = join(join(boss_dir,'settings'), 'op_settings.json')
op_settings = json_loadPath(op_settings_json_path)

draw_mode = op_settings['draw_mode']

del boss_dir
del op_settings_json_path
del op_settings

class Boss_OT_base_ui(bpy.types.Operator):
    bl_idname = "boss.base_ui"
    bl_label = "Base UI"

    def onTimerTick(self):
        if self.isCursorRunning:
            self.cursor_counter += 1
            if self.cursor_counter % 2 == 0:
                self.uip._canDrawCursor = True
            else:
                self.uip._canDrawCursor = False

    def _cleanUp(self):
        uip = self.uip

        self._temp_all_drawable = None

        uip.deleteImageFiles()
        uip.reset()
        NormalInput.mouseEntered.clear()

    def _removeHandle(self):
        if self._handle:
            SpaceType.from_str(self.space_type).value.draw_handler_remove(self._handle, 'WINDOW')
            self._handle = None

    def modal(self, context, event):
        try:
            if self._cancelModal:
                return {'CANCELLED'}

            start_time = time.perf_counter()
            context.area.tag_redraw()
            uip = self.uip
            if uip.keyboardInput:
                TextFieldInput.takeTextFieldInput(uip, event)
                if event.type == 'TIMER':
                    self.onTimerTick()
            else:
                NormalInput.takeNormalInput(self, event, uip)

            self.modalTime = (time.perf_counter() - start_time)

            self.modal_after()

            return {'RUNNING_MODAL'}
        except Exception as e:
            print('*' * 25, 'Modal failed: ', '*' * 25)
            str_e = str(e)
            self.msg(f'{e}, ...Modal Failed, check console for details', 2)
            print(str_e)
            print(traceback.format_exc())
            print('*' * 50)

            self.quit()
            return {'CANCELLED'}

    def modal_after(self):
        pass

    def quit(self):
        self._removeHandle()
        self._cleanUp()

        for fn in self.onCancel:
            fn()
        self._cancelModal = True

    def finish(self):
        self._removeHandle()
        self._cleanUp()

        for fn in self.onFinish:
            fn()

        self._cancelModal = True

    def ui_setup_before(self):
        pass

    def ui_setup_after(self):
        pass

    def ui_elements(self):
        pass

    def getAllowedSpaceTypes(self) -> set:
        return {SpaceType.VIEW_3D.name, }

    def msg(self, text: str, messageType=0):
        self.report(msgType[messageType], text)

    def invoke(self, context, event):
        try:
            start_time = time.perf_counter()

            self.space_type = context.area.type

            if self.space_type in self.getAllowedSpaceTypes():
                self._temp_all_drawable = None
                self._cancelModal = False
                self.isCursorRunning = False
                self.modalTime = 0

                self.onFinish = []
                self.onCancel = []

                self.display_text:List[HudText] = []

                self.ui_setup_before()
                self.uip = uiParams(self)

                uip = self.uip
                uip.context = context

                uip.escapeFn.append(self.quit)

                uip.dict_styles = getStylesDict()

                uip.curStyle = loadStyle(uip.dict_styles[uip.curStyleName])

                uip.mouse_x = event.mouse_region_x
                uip.mouse_y = event.mouse_region_y
                uip.region_width = context.region.width
                uip.region_height = context.region.height
                uip.region_rect = RectData(0, 0, uip.region_width, uip.region_height)
                uip.dict_imgs = get_dict_imageName_imagePath()

                self.ui_setup_after()

                self._dx = 0  
                self._dy = 0

                self.cursor_counter = 0

                self.draw_debug: bool = True

                if uip.use_hierarchy:
                    self.rootPanel = Panel(
                        self,
                        uip.region_rect.copy(),
                        PanelData.with_defaults()
                    )

                self.ui_elements()

                args = (self,)

                self._handle = None

                if draw_mode == 'optimized':
                    drawing_callback = drawing_callbacks.draw_callback_px_optimized
                else:
                    drawing_callback = drawing_callbacks.draw_callback_px

                self._handle = SpaceType.from_str(self.space_type).value.draw_handler_add(drawing_callback, args, 'WINDOW', 'POST_PIXEL')

                context.window_manager.modal_handler_add(self)
                return {'RUNNING_MODAL'}
            else:
                self.msg("Area is not in getAllowedSpaceTypes",1)
                return {'CANCELLED'}

        except Exception as e:
            print('*' * 25, 'Invoke Failed: ', '*' * 25)
            str_e = str(e)
            print(str_e)

            self.msg(f'{e} ... Invoke Failed, check console for details',2)
            print(traceback.format_exc())
            print('*' * 50)

            return {'CANCELLED'}


