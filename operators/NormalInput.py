btnsToDrag : list
from .uiParams import uiParams

mouseEntered = []

def takeNormalInput(op,event,uip:uiParams):
    global btnsToDrag
    global mouseEntered

    uip.mouse_x = event.mouse_region_x
    uip.mouse_y = event.mouse_region_y

    if uip.use_hierarchy:
        if not op.rootPanel.rectData.isPointInside(uip.mouse_x,uip.mouse_y):
            return

        if event.type == 'WHEELUPMOUSE':
            op.rootPanel.check_mouse_enter_exit_hierarchy(uip.mouse_x,uip.mouse_y)
            op.rootPanel._onWheelUp_hierarchy(uip.mouse_x,uip.mouse_y)

        elif event.type == 'WHEELDOWNMOUSE':
            op.rootPanel.check_mouse_enter_exit_hierarchy(uip.mouse_x, uip.mouse_y)
            op.rootPanel._onWheelDown_hierarchy(uip.mouse_x, uip.mouse_y)

        if(event.type == 'LEFTMOUSE'):
            if(event.value == 'PRESS'):
                uip.mouse_down_x = uip.mouse_x
                uip.mouse_down_y = uip.mouse_y

                if not uip._btnToDrag:
                    btnsToDrag = []

                    for ui in uip.ui_onDragBegin:
                        if ui.rectData.isPointInside(uip.mouse_x,uip.mouse_y):
                            if ui.clipRect:
                                if ui.clipRect.isPointInside(uip.mouse_x,uip.mouse_y):
                                    btnsToDrag.append(ui)
                            else:
                                btnsToDrag.append(ui)

                if len(btnsToDrag) > 0:
                    uip._btnToDrag = sorted(btnsToDrag, key=lambda x: x.gui_depth, reverse=True)[0]
                    uip._btnToDrag._onDragBegin()

            elif(event.value == 'RELEASE'):
                if uip._btnToDrag:
                    uip._btnToDrag._onDragEnd()

                uip._btnToDrag = None

                if uip.mouse_down_x == uip.mouse_x and uip.mouse_down_y == uip.mouse_y:
                    onClicks = []

                    for btn in uip.ui_onClick:
                        if btn.rectData.isPointInside(uip.mouse_x,uip.mouse_y):
                            onClicks.append(btn)

                    if len(onClicks) > 0:
                        sortedButtons = sorted(onClicks, key=lambda x: x.gui_depth, reverse=True)
                        for btn in sortedButtons:
                            if btn.clipRect == None:
                                btn._onClick()
                                break
                            elif btn.clipRect.isPointInside(uip.mouse_x,uip.mouse_y):
                                btn._onClick()
                                break

                    else:
                        if uip.color_picker_fn:
                            if not uip.color_picker.bgPanelBtn.rectData.isPointInside(uip.mouse_x,uip.mouse_y):
                                uip.color_picker_fn()

        elif(event.type == 'MOUSEMOVE'):
            if uip._btnToDrag:
                op._dx = uip.mouse_x - uip.mouse_down_x
                op._dy = uip.mouse_y - uip.mouse_down_y
                uip._btnToDrag._onDrag(op._dx, op._dy)

            for ui in uip.ui_onMouseEnter:
                ui.check_mouse_enter_exit(uip.mouse_x, uip.mouse_y)

        if event.type == 'RIGHTMOUSE':
            if event.value == 'RELEASE':
                lastEsc = uip.escapeFn.pop()
                lastEsc()

        if event.type == 'ESC':
            if event.value == 'RELEASE':
                lastEsc = uip.escapeFn.pop()
                lastEsc()

    else:
        if event.type == 'WHEELUPMOUSE':
            processMouseExit(uip)
            processMouseEnter(uip)
            for ui in uip.ui_onWheelUp:
                if ui.clipRect:
                    if ui.clipRect.isPointInside(uip.mouse_x, uip.mouse_y):
                        if ui.rectData.isPointInside(uip.mouse_x,uip.mouse_y):
                            ui._onWheelUp()
                else:
                    if ui.rectData.isPointInside(uip.mouse_x, uip.mouse_y):
                        ui._onWheelUp()

        elif event.type == 'WHEELDOWNMOUSE':
            processMouseExit(uip)
            processMouseEnter(uip)
            for ui in uip.ui_onWheelDown:
                if ui.clipRect:
                    if ui.clipRect.isPointInside(uip.mouse_x, uip.mouse_y):
                        if ui.rectData.isPointInside(uip.mouse_x,uip.mouse_y):
                            ui._onWheelDown()
                else:
                    if ui.rectData.isPointInside(uip.mouse_x, uip.mouse_y):
                        ui._onWheelDown()

        if(event.type == 'LEFTMOUSE'):
            if(event.value == 'PRESS'):
                uip.mouse_down_x = uip.mouse_x
                uip.mouse_down_y = uip.mouse_y

                if not uip._btnToDrag:
                    btnsToDrag = []

                    for ui in uip.ui_onDragBegin:
                        if ui.rectData.isPointInside(uip.mouse_x,uip.mouse_y):
                            if ui.clipRect:
                                if ui.clipRect.isPointInside(uip.mouse_x,uip.mouse_y):
                                    btnsToDrag.append(ui)
                            else:
                                btnsToDrag.append(ui)

                if len(btnsToDrag) > 0:
                    uip._btnToDrag = sorted(btnsToDrag, key=lambda x: x.gui_depth, reverse=True)[0]
                    uip._btnToDrag._onDragBegin()

            elif(event.value == 'RELEASE'):
                if uip._btnToDrag:
                    uip._btnToDrag._onDragEnd()

                uip._btnToDrag = None

                if uip.mouse_down_x == uip.mouse_x and uip.mouse_down_y == uip.mouse_y:
                    onClicks = []

                    for btn in uip.ui_onClick:
                        if btn.rectData.isPointInside(uip.mouse_x,uip.mouse_y):
                            onClicks.append(btn)

                    if len(onClicks) > 0:
                        sortedButtons = sorted(onClicks, key=lambda x: x.gui_depth, reverse=True)
                        for btn in sortedButtons:
                            if btn.clipRect == None:
                                btn._onClick()
                                break
                            elif btn.clipRect.isPointInside(uip.mouse_x,uip.mouse_y):
                                btn._onClick()
                                break

                    else:
                        if uip.color_picker_fn:
                            if not uip.color_picker.bgPanelBtn.rectData.isPointInside(uip.mouse_x,uip.mouse_y):
                                uip.color_picker_fn()

        elif(event.type == 'MOUSEMOVE'):
            if uip._btnToDrag:
                op._dx = uip.mouse_x - uip.mouse_down_x
                op._dy = uip.mouse_y - uip.mouse_down_y
                uip._btnToDrag._onDrag(op._dx, op._dy)

            processMouseExit(uip)
            processMouseEnter(uip)

        if event.type == 'RIGHTMOUSE':
            if event.value == 'RELEASE':
                lastEsc = uip.escapeFn.pop()
                lastEsc()

        if event.type == 'ESC':
            if event.value == 'RELEASE':
                lastEsc = uip.escapeFn.pop()
                lastEsc()

def processMouseEnter(uip):
    for ui in uip.ui_onMouseEnter:
        newIsMouseInside = ui.rectData.isPointInside(uip.mouse_x, uip.mouse_y)
        if ui.clipRect:
            if ui.clipRect.isPointInside(uip.mouse_x, uip.mouse_y):
                if not ui._isMouseInside:
                    if newIsMouseInside:
                        ui._isMouseInside = True
                        mouseEntered.append(ui)
                        ui._onMouseEnter()
                    else:
                        pass
        else:
            if not ui._isMouseInside:
                if newIsMouseInside:
                    ui._isMouseInside = True
                    mouseEntered.append(ui)
                    ui._onMouseEnter()
                else:
                    pass

def processMouseExit(uip):
    global mouseEntered
    for ui in mouseEntered[:]:
        newIsMouseInside = ui.rectData.isPointInside(uip.mouse_x, uip.mouse_y)
        if newIsMouseInside:
            pass
        else:
            ui._isMouseInside = False
            ui._onMouseExit()
            mouseEntered.remove(ui)

