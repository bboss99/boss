import blf
from . Alignment import Align

__all__ = ['TextData','Text']

class TextData():
    def __init__(self, fontSize=-1, font_id=-1, align=None, color=None):
        self.fontSize   = fontSize

        self.font_id    = font_id
        self.align      = align if isinstance(align, Align) else Align.from_str(align)
        self.color      = color

    def __str__(self):
        return "textData - fontSize - {},{}, font_id - {},{}, align - {},{}, color - {},{}".\
            format( type(self.fontSize),self.fontSize,type(self.font_id),self.font_id,
                    type(self.align),self.align,type(self.color),self.color)

    @classmethod
    def with_defaults(cls, fontSize = 15, font_id = 0, align = Align.Center,color = None):
        return cls(fontSize,font_id,align,color)

class Text():
    def __init__(self, text = '', rectData = None, textData = None, clipRect = None):
        self.text           = text
        self.rectData       = rectData  
        self.textData       = textData if textData else TextData.with_defaults()
        self.clipRect       = clipRect  
        self.onTextChanged() 

    def setText(self,text):
        self.text = text
        self.onTextChanged()

    def setTextAlignment(self, alignment):
        self.textData.align = alignment
        self.onTextChanged()

    def setTextColor(self, color):
        self.textData.color = color

        pass

    def setTextFontSize(self, fontSize):
        self.textData.fontSize = fontSize
        self.onTextChanged()

    def onTextChanged(self):
        self.setDimension()
        self.setTextPosition()

    def setDimension(self):
        blf.size(self.textData.font_id, self.textData.fontSize, 72)
        self.textWidth, self.textHeight = blf.dimensions(self.textData.font_id, self.text) 

    def getTextSize(self):
        return blf.dimensions(self.textData.font_id,self.text)

    def setRectData(self, rectData):
        self.rectData = rectData

    def setTextPosition(self):
        xCenter = (self.rectData.xMin + self.rectData.xMax ) / 2
        yCenter = (self.rectData.yMin + self.rectData.yMax ) / 2
        
        align =  self.textData.align.value 

        if align == Align.Center.value:
            self.xPos   = xCenter  - self.textWidth/2
            self.yPos   = yCenter  - self.textHeight/2
        
        elif align == Align.BL.value:
            self.xPos   = self.rectData.xMin
            self.yPos   = self.rectData.yMin
        
        elif align == Align.Left.value:
            self.xPos   = self.rectData.xMin
            self.yPos   = yCenter - self.textHeight/2

        elif align == Align.TL.value:
            self.xPos   = self.rectData.xMin
            self.yPos   = self.rectData.yMax - self.textHeight
        
        elif align == Align.Top.value:
            self.xPos   = xCenter  - self.textWidth/2
            self.yPos   = self.rectData.yMax - self.textHeight

        elif align == Align.TR.value:
            self.xPos   = self.rectData.xMax  - self.textWidth
            self.yPos   = self.rectData.yMax - self.textHeight

        elif align == Align.Right.value:
            self.xPos   = self.rectData.xMax  - self.textWidth
            self.yPos   = yCenter - self.textHeight/2

        elif align == Align.BR.value:
            self.xPos   = self.rectData.xMax  - self.textWidth
            self.yPos   = self.rectData.yMin

        elif align == Align.Bottom.value:
            self.xPos   = xCenter  - self.textWidth/2
            self.yPos   = self.rectData.yMin

    def setClipRect(self, clipRect):
        self.clipRect = clipRect

    def draw(self):
        if self.clipRect:
            self.draw_clipped()
        else:
            self.draw_normal()

    def draw_normal(self):
        blf.size(self.textData.font_id, self.textData.fontSize, 72)

        if self.textData.color:
            blf.color(self.textData.font_id, *self.textData.color)

        blf.position(self.textData.font_id, self.xPos, self.yPos , 0)
        blf.draw(self.textData.font_id, self.text)

    def draw_clipped(self):
        blf.size(self.textData.font_id, self.textData.fontSize, 72)

        blf.enable(self.textData.font_id, blf.CLIPPING)

        blf.clipping(self.textData.font_id, * self.clipRect._clipRect)

        if self.textData.color:
            blf.color(self.textData.font_id, *self.textData.color)

        blf.position(self.textData.font_id, self.xPos, self.yPos , 0)
        blf.draw(self.textData.font_id, self.text)

        blf.disable(self.textData.font_id, blf.CLIPPING )
