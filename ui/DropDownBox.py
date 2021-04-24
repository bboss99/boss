
from ..Geo.RectData import RectData

from . Button import ButtonData,Button
from . Panel import Panel
from .base_ui.PanelData import PanelData
from .. Layout import VerticalLayout
from .. Text import TextData
from ..Color import Color
from .. utils import _addCallback, removeCheckFunc
from itertools import chain

__all__ = ['DropDownBox']

class DropDownBox():
    def __init__(self,op,rectData=None,panelData=None,textList=None,imageList=None,toolTips=None,defaultIndex=0,onValueChange=None):
        self.op                 = op

        self.panelData          = panelData if panelData else PanelData()
        self.panelData.panelType= 'DropDownBox'
        
        self.textList           = textList
        self.imageList          = imageList
        self.toolTips           = toolTips

        self.defaultIndex       = defaultIndex
        self.selectedIndex      = defaultIndex
        
        if self.textList:
            self.panelData.text     = self.textList[self.defaultIndex]
            self.panelData.textData = self.panelData.textData if self.panelData.textData else TextData.with_defaults()
        else:
            self.panelData.text     = ''

        self.panelData.image_path= self.imageList[self.defaultIndex] if self.imageList else ''

        self.mainButton         = Button(
                                    self.op,
                                    rectData, 
                                    self.panelData,
                                    ButtonData(
                                        onClick = self.showOptionsMenu
                                        )
                                    )

        self.element_height     = self.mainButton.rectData.height

        self.onValueChanged     = []
        self.add_onValueChanged(onValueChange)

        self.rowCount           = len(textList) if textList else len(imageList)        
        self._totalButtonsHeight= self.element_height*self.rowCount

        self.needsClipRect      = False  
        self._options           = []  
    
    def showOptionsMenu(self,*param):
        if len(self._options) > 0:
            self.deletePopUp()
            return
        rectData = self.mainButton.rectData
        
        buttonsParent   = None
        rds             = None

        self.needsClipRect   = False
        if self._totalButtonsHeight < self.mainButton.yMin:
            firstRD = RectData(rectData.xMin,rectData.yMin-rectData.height,rectData.width,rectData.height)
            rds = VerticalLayout.GetRectDataListFrom(firstRD,len(self.textList),False)

        elif self._totalButtonsHeight < (self.op.uip.region_rect.yMax - self.mainButton.yMax):
            firstRD = RectData(rectData.xMin,rectData.yMin+rectData.height,rectData.width,rectData.height)
            rds = VerticalLayout.GetRectDataListFrom(firstRD,len(self.textList),True)

        else:
            self.needsClipRect   = True
            firstRD = RectData(rectData.xMin,rectData.yMin-rectData.height,rectData.width,rectData.height)

            rds = VerticalLayout.GetRectDataListFrom(firstRD,len(self.textList),False)
            
            parentDragRect_RD           = RectData(
                                                firstRD.xMin,
                                                firstRD.yMin,
                                                firstRD.width,
                                                self._totalButtonsHeight - firstRD.yMin
                                            )
            self.buttonsParentPanel     = Panel(
                                            self.op,
                                            firstRD,
                                            PanelData(
                                                canDrag=False,
                                                text='buttonsParentPanel',
                                                normal_color=Color.GRAY_M04,
                                                hover_color=Color.GRAY_M04,
                                                parent=self.mainButton,
                                                rectIsLocal=False,
                                                dragRect=parentDragRect_RD
                                                )
                                            )
        
            self.clippingRectButton     = Button(
                                                self.op,
                                                RectData(
                                                    firstRD.xMin,
                                                    0,
                                                    firstRD.width,
                                                    firstRD.yMax
                                                ),
                                                PanelData(
                                                    text='clippingPlane',
                                                    parent=None,
                                                    canDrag=False
                                                    ),
                                                ButtonData(
                                                    onWheelDown= (self._onWheelRolled,0, 50),
                                                    onWheelUp = (self._onWheelRolled,0, -50),
                                                )
                                            )
            buttonsParent               = self.buttonsParentPanel

            self.buttonsParentPanel.canDraw = False 
            self.clippingRectButton.canDraw = False 
        
        for i, (text,rd) in enumerate(zip(self.textList,rds)):
            self._options.append(
                Button(
                    self.op,
                    rd,
                    PanelData(
                        text=text,
                        parent=buttonsParent,
                        rectIsLocal=False,
                        clipRect=self.clippingRectButton.rectData if self.needsClipRect else None,
                        canDrag=False,
                        panelType='DropDownBoxOption'
                        ),
                    ButtonData(onClick=(self.optionButtonClicked,i))
                )
            )        

    def _onWheelRolled(self,x,y):
        self.buttonsParentPanel.shiftPanelPosition(x,y)

    def add_onValueChanged(self,*params):
        _addCallback(self,self.onValueChanged,*params)

    def remove_onValueChanged(self,func):
        removeCheckFunc(self.onValueChanged,func)

    def optionButtonClicked(self,*param):        
        if self.selectedIndex == param[0]:
            pass
        else:
            self.setValue( param[0] )        
        self.deletePopUp()

    def getSelectedText(self):
        return self.textList[self.selectedIndex]
    
    def setValue(self,index):
        self.selectedIndex = index
        self.mainButton._text.setText( self.textList[self.selectedIndex] )
        self._onValueChanged()
    
    def _onValueChanged(self):
        print('_onValueChange')
        for fn in self.onValueChanged:
            fn()

    def deletePopUp(self):        
        if self.needsClipRect:
            self.buttonsParentPanel.deleteUI()
            self.clippingRectButton.deleteUI()
            self.needsClipRect = False
            
        for each in reversed(self._options):
            self._options.remove(each)
            each.deleteUI()
 
    def getPanels(self):
        return [self.buttonsParentPanel] if self.needsClipRect else []

    def getButtons(self):
        return [self.mainButton] + (self._options if self._options else []) + ([self.clippingRectButton] if self.needsClipRect else [])

    def setEnabledState(self, enableState = True, pCallbacks=True, pDrawable = True):        
        if enableState:
            self.enable(pCallbacks,pDrawable)
        else:
            self.disable(pCallbacks,pDrawable)
    
    def enable(self,pCallbacks=True,pDrawable = True):
        for each in chain(self.getPanels(),self.getButtons()):
            each.enable(pCallbacks,pDrawable)

    def disable(self,pCallbacks=True,pDrawable = True):
        for each in chain(self.getPanels(),self.getButtons()):
            each.disable(pCallbacks,pDrawable)

