from itertools import chain
class uiBase():
    def getPanels(self):
        return []

    def getButtons(self):
        return []
    
    def setEnabledState(self, enableState = True, pCallbacks=True, pDrawable = True):        
        if enableState:
            self.enable(pCallbacks,pDrawable)
        else:
            self.disable(pCallbacks,pDrawable)
    
    def enable(self,pCallbacks=True,pDrawable = True):
        for each in chain(self.getPanels(), self.getButtons()):
            each.enable(pCallbacks,pDrawable)

    def disable(self,pCallbacks=True,pDrawable = True):
        for each in chain(self.getPanels(), self.getButtons()):
            each.disable(pCallbacks,pDrawable)

