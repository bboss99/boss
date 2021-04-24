from . import Boss_OT_base_ui
from . import uiParams
from itertools import chain
import bgl
import blf
import traceback

import boss.utils as boss_utils

style = boss_utils.loadStyle(boss_utils.getStylesDict()['style_01'])

g_font_id = style.get('GlobalFontId', 0)
g_font_size = style.get('GlobalFontSize', 15)
g_font_color = style.get('GlobalFontColor', 15)
g_dpi = style.get('GlobalFontDpi', 72)

del style
del boss_utils

def draw_text_atPos(texts, pos=(0, 0), space=10, direction='up', color=(1, 1, 1, 1), font_size=None, font_id=None):
    font_id1 = font_id if font_id else g_font_id
    blf.size(font_id1, font_size if font_size else g_font_size, g_dpi)
    blf.color(font_id1, *color)

    if direction == 'down':
        space = -space

    for i, text in enumerate(texts):
        blf.position(font_id1, pos[0], pos[1] + space * i, 0)
        blf.draw(font_id1, text)

def showGlobalTextToolTip(uip):
    blf.size(g_font_id, 20, g_dpi)
    gtt = uip.globalToolTip
    tttx, ttty = uip.get_ttt_anchor_co()
    if isinstance(gtt, (list,tuple)):
        toolTip_x = tttx + uip.toolTipOffset[0]
        toolTip_y = ttty + uip.toolTipOffset[1]

        for i, text in enumerate(reversed(gtt)):
            blf.position(g_font_id, toolTip_x, toolTip_y + 30 * i, 0)
            blf.draw(g_font_id, text)
    else:
        blf.position(g_font_id, tttx + uip.toolTipOffset[0], ttty + uip.toolTipOffset[1], 0)
        blf.draw(g_font_id, gtt)

def showGlobalImageToolTip(uip: uiParams.uiParams):
    ttix,ttiy = uip.get_tti_anchor_co()

    uip.globalToolTipPanel.setPosition(
        ttix + uip.panelToolTipOffsets[0],
        ttiy + uip.panelToolTipOffsets[1]
    )

    uip.globalToolTipPanel.draw()

    pass

def draw_callback_px_optimized(op:Boss_OT_base_ui):
    uip:uiParams.uiParams = op.uip

    bgl.glEnable(bgl.GL_BLEND)

    try:
        _shader = None
        for panel in uip.ui_drawable:
            geo = panel.geo

            if not geo:
                continue

            batch = geo._batched if geo._batched else geo.newbatch()

            if _shader == geo.shader:
                pass
            else:
                _shader = geo.shader
                _shader.bind()

            if geo.geoData.image_path == '':
                pass
            else:
                bgl.glActiveTexture(bgl.GL_TEXTURE0)
                bgl.glBindTexture(bgl.GL_TEXTURE_2D, geo.imageData.bindcode)

                geo.shader.uniform_int("image", 0)

            if geo.clipRect:
                geo.shader.uniform_float(
                    'clipRect',
                    panel.clipRect._clipRect
                )
            batch.draw(geo.shader)

        _shader = None

        blf.size(g_font_id, g_font_size, g_dpi)
        blf.color(g_font_id, *g_font_color)

        is_clipping_enabled = False

        for panel in uip.ui_drawable_texts:
            t = panel._text

            blf.position(g_font_id, t.xPos, t.yPos, 0)

            if t.clipRect:
                if is_clipping_enabled:
                    pass
                else:
                    blf.enable(g_font_id, blf.CLIPPING)
                    is_clipping_enabled = True
                blf.clipping(g_font_id, *t.clipRect._clipRect)
            else:
                if is_clipping_enabled:
                    blf.disable(g_font_id, blf.CLIPPING)
                    is_clipping_enabled = False

            blf.draw(g_font_id, t.text)

        if is_clipping_enabled:
            blf.disable(g_font_id, blf.CLIPPING)

    except Exception as e:
        print('*' * 25, 'Drawing failed: ', '*' * 25)
        op.msg(f'{e} ... Drawing Failed, check console for details', 2)
        print(str(e))
        print(traceback.format_exc())
        print('*' * 25, 'drawing failed: ', '*' * 25)
        op.quit()

    if op.display_text:
        for dt in op.display_text:
            dt.draw()

    if uip.globalToolTipImagePath:
        showGlobalImageToolTip(uip)

    if uip.globalToolTip:
        showGlobalTextToolTip(uip)

    if uip._canDrawCursor:
        uip.cursor.draw()

    bgl.glDisable(bgl.GL_BLEND)

def draw_callback_px(op):
    uip = op.uip
    try:
        if uip.ui_drawable_dirty or uip.ui_drawable_texts_dirty:
            op._temp_all_drawable = list(chain(uip.ui_drawable, set(uip.ui_drawable_texts) - set(uip.ui_drawable)))
            uip.ui_drawable_dirty = False
            uip.ui_drawable_texts_dirty = False

        for ui in op._temp_all_drawable:
            ui.draw()

    except Exception as e:
        print('*' * 25, 'drawing failed: ', '*' * 25)
        print(str(e))
        print(traceback.format_exc())
        print('*' * 25, 'drawing failed: ', '*' * 25)
        op._cancelModal = True

    if op.display_text:
        for dt in op.display_text:
            dt.draw()

    if uip.globalToolTipImagePath:
        showGlobalImageToolTip(uip)

    if uip.globalToolTip:
        showGlobalTextToolTip(uip)

    if uip._canDrawCursor:
        uip.cursor.draw()


