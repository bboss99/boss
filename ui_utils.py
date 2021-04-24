import blf

def getTextSize(font_id,text):
    return blf.dimensions(font_id,text)

def getTextsSize(font_id,texts):
    return zip(*[blf.dimensions(font_id,t) for t in texts])

def guiDepth_setAfter(allGuiElements,guiToSet, toSetAfter):
    sorted_allGuiElements = sorted(allGuiElements, key=lambda x: x.gui_depth, reverse=False)
    
    print([i.gui_depth for i in sorted_allGuiElements])
    return

    toSetAfter_index       = allGuiElements.index(toSetAfter)
    toSetAfter_gui_depth   = toSetAfter.gui_depth
    guiToSet_gui_depth     = guiToSet.gui_depth

    if guiToSet_gui_depth > toSetAfter_gui_depth:
        return

    pass

def guiDepth_setBefore(allGuiElements,guiToSet, toSetBefore):
    toSetBefore_index       = allGuiElements.index(toSetBefore)
    toSetBefore_gui_depth   = toSetBefore.gui_depth
    guiToSet_gui_depth      = guiToSet.gui_depth

    if guiToSet_gui_depth < toSetBefore_gui_depth:
        return

    guiToSet.gui_depth = toSetBefore_gui_depth

    for ge in allGuiElements[toSetBefore_index:]:
        if not ge == guiToSet:
            ge.gui_depth += 1

def guiDepths_sort(guiElements):
    gui_depths          = [ge.gui_depth for ge in guiElements]
    sorted_gui_depths   = sorted(gui_depths)
    
    for ge, sgd in zip(guiElements,sorted_gui_depths):
        ge.gui_depth = sgd

def guiElements_getSorted_placeBefore(allGuiElements,guiToPlace,placeBeforeThis):
    guiToPlaceIndex         = allGuiElements.index(guiToPlace)
    placeBeforeThisIndex    = allGuiElements.index(placeBeforeThis)

    removedObj              = allGuiElements.pop(guiToPlaceIndex)
    
    allGuiElements.insert(placeBeforeThisIndex,removedObj)

def guiElements_getSorted_Inplace(allGuiElements,guiElements):
    indices = [i for i,ge in enumerate(allGuiElements) if ge in guiElements]

    for index,ge in zip(indices,guiElements):
        allGuiElements[index] = ge

def guiElements_getSorted_BringToFront(allGuiElements,guiElements):
    allGE_Minus_GE= [ge for ge in allGuiElements if ge not in guiElements]
    newGuiList = allGE_Minus_GE.extend(guiElements)


