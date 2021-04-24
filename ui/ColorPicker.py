from boss.Color import Color
from boss.ui.Slider import Slider
from boss.Geo.RectData import RectData
from boss.ui.base_ui.PanelData import PanelData
from boss.ui.Panel import Panel
from boss.ui.Button import ButtonData, Button
from math import sqrt,pi,degrees
from boss.math.Vector2D import Vector2D
from itertools import chain

def getWheelColor(pointCount,hueStep):
    return [Color.WHITE]+[Color.change(Color.RED, hueStep * i, True) for i in range(pointCount)]

class ColorPicker():
    def __init__(self,op,width,colorRGBA  = Color.GRAY,indicatorSize = 8,pointCount = 16):
        self.op                     = op

        self.uip                     = op.uip  

        self.width                  = width

        self.enabled                = True

        self.indicatorSize          = indicatorSize
        self.pointCount             = pointCount

        self.hueStep                = 1/self.pointCount

        self.onColorUpdate          = []

        self.bgPanelBtn             = Button(
                                            self.op,
                                            RectData(),
                                            PanelData(
                                                canDrag=True,
                                                normal_color=Color.GRAY_M02,
                                                panelType='ColorField'
                                            ),
                                            ButtonData()
                                        )

        self.setColor_fromRGBA(colorRGBA)

        wheelButtonRD               = RectData()
        self.wheelButton            = Button(
                                            self.op,
                                            wheelButtonRD,
                                            PanelData(
                                                parent=self.bgPanelBtn,
                                                canDrag=True,
                                                geo_type='CIR',
                                                normal_color=getWheelColor(self.pointCount,self.hueStep),
                                                hover_color=None,
                                                panelType='ColorField',
                                                dragRect=wheelButtonRD
                                            ),
                                            ButtonData(
                                                onDragBegin=(self.removeUpdateVerts,'add'),
                                                onDragEnd=(self.removeUpdateVerts,'remove'),
                                                onDrag=self.onWheelBgDragged,
                                                onClick=self.onWheelBgDragged
                                            )
                                        )

        self.geo                    = self.wheelButton.geo  

        self.valueSlider         = Slider(self.op,RectData(),PanelData(parent=self.bgPanelBtn),
                                            0,0,1,False,onValueChange=self.onColorValueChange
                                            )

        self.alphaSlider            = Slider(self.op,RectData(),PanelData(parent=self.bgPanelBtn),
                                            0,0,1,False,onValueChange=self.onAlphaChange
                                            )

        gradientColor = [ Color.BLACK,Color.WHITE,Color.WHITE,Color.BLACK ]

        self.valueSlider.sliderBase.geo.setColor( gradientColor )
        self.alphaSlider.sliderBase.geo.setColor( gradientColor )

        self.wheelIndicatorPanel    = Panel(
                                        self.op,
                                        RectData(0,0,indicatorSize,indicatorSize),
                                        PanelData(
                                            normal_color=Color.WHITE,
                                            geo_type='Rect',
                                            panelType='none',
                                            parent=self.bgPanelBtn,
                                        )
                                    )

        self._setDimensions()
        self.setIndicatorFromSelectedColor()

        self.valueSlider.setValue(self.valueSlider.getValue(), callCallback=True)

    def removeUpdateVerts(self,*param):
        if param[0] == 'add':
            self.wheelButton.rectData.add_onUpdate(self.geo.updateVerts)
        else:
            self.wheelButton.rectData.remove_onUpdate(self.geo.updateVerts)
    
    def _setDimensions(self):
        valueSliderWidth = self.width * .1
        sliderGap = valueSliderWidth*.25

        otherFieldsHeight = 0 

        self.bgPanelBtn.setPositionAndSize(
            0,
            0,
            self.width + valueSliderWidth + sliderGap + valueSliderWidth ,
            self.width + otherFieldsHeight
        )
        
        self.wheelButton.setPositionAndSize(
            0,
            otherFieldsHeight,
            self.width,
            self.width
        )
        
        self.wheelButton.geo.recalculateVerts()

        self.valueSlider.setPositionAndSize(
            RectData(
                self.width,
                otherFieldsHeight,
                valueSliderWidth,
                self.width
            )
        )
        
        self.alphaSlider.setPositionAndSize(
            RectData(
                self.width + valueSliderWidth + sliderGap,
                otherFieldsHeight,
                valueSliderWidth,
                self.width
            )
        )

        pass
    
    def setPositionAndSize(self,xPos,yPos):
        pass
    
    def setPosition(self,xMin,yMin):
        self.bgPanelBtn.setPositionWithChildren(xMin,yMin)

        pass
 
    def setColor_fromRGBA(self,rgba):
        self.colorRGBA  = rgba
        self.colorHSV   = Color.rgb_to_hsv(*rgba[:-1])
        self.value      = self.colorHSV[-1]
        self.alpha      = rgba[-1]

        self.bgPanelBtn.geo.setColor(self.colorRGBA)

        for fn in self.onColorUpdate:
            fn()

    def setColor_fromHSV(self,hsv):        
        self.setColor_fromRGBA(
            ( *Color.hsv_to_rgb(*hsv), self.alpha )
            )       

    def setColor_fromValue(self,value):
        self.setColor_fromHSV(
             (*self.colorHSV[:-1],value) 
             )

    def setColor_fromAlpha(self,alpha):        
        self.setColor_fromRGBA( ( *self.colorRGBA[:-1] , alpha ) )

    def setIndicatorFromSelectedColor(self):
        r, g, b, a = self.colorRGBA
        h, s, v = Color.rgb_to_hsv(r, g, b)

        hueAngle        = h*360  

        center          = Vector2D.from_tuple(self.geo.center)
        
        initDir         = Vector2D(center.x,-1000)

        indicatorPoint  = Vector2D.rotate_point( center , initDir , hueAngle )

        hueDir          = indicatorPoint - center

        hueDirNormal    = hueDir.normalized()

        indicatorPoint  = center + hueDirNormal*self.geo.radius * s

        self.wheelIndicatorPanel.setPosition(indicatorPoint.x - self.indicatorSize/2,indicatorPoint.y-self.indicatorSize/2)

        self.valueSlider.setValue(v,callCallback=False)
        self.alphaSlider.setValue(a,callCallback=False)

    def setColorFromMouseLocation(self):
        center          = Vector2D.from_tuple(self.geo.center)

        mousePos        = Vector2D(self.uip.mouse_x ,self.uip.mouse_y)

        centerToMouse   = mousePos - center

        initVector      = Vector2D(0,-1000)

        mouseAngle      = Vector2D.angle(initVector,centerToMouse)

        if mouseAngle < 0 :
            mouseAngle = pi*2 + mouseAngle

        hue = mouseAngle / (2 * pi)
        
        sat = centerToMouse.magnitude/self.geo.radius

        if sat > 1:
            sat = 1

        self.setColor_fromHSV( (hue,sat,self.value) )
        self.setIndicatorFromSelectedColor()

    def onWheelBgDragged(self):
        self.setColorFromMouseLocation()
 
    def onColorValueChange(self,caller):
        self.setColor_fromValue(caller.value)        
        
        nonZeroValue = max(caller.value,.001)
        newVertColors = [ ( *Color.rgb_setValue(each[:-1],nonZeroValue ), 1 )  for each in self.geo.vertex_colors]
        
        self.geo.setColor(newVertColors)

    def onAlphaChange(self,caller):
        self.setColor_fromAlpha(caller.value)

    def getPanels(self):
        return [self.wheelIndicatorPanel]

    def getButtons(self):
        return [self.bgPanelBtn,self.wheelButton] + self.valueSlider.getButtons() +  self.alphaSlider.getButtons()

    def setEnabledState(self, enableState = True, pCallbacks=True, pDrawable = True):        
        if enableState:
            self.enable(pCallbacks,pDrawable)
        else:
            self.disable(pCallbacks,pDrawable)

    def enable(self,pCallbacks=True,pDrawable = True):
        self.enabled = True

        for each in chain(self.getButtons(), self.getPanels()):
            each.enable(pCallbacks,pDrawable)

    def disable(self,pCallbacks=True,pDrawable = True):
        self.enabled = False
        for each in chain(self.getButtons(), self.getPanels()):
            each.disable(pCallbacks,pDrawable)

