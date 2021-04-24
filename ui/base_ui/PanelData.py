from __future__ import annotations
from ...Geo.base_geo.GeoData import GeoData
from ... utils import copy
from ... Text import TextData
from typing import Union, Callable, List

__all__ = ['PanelData']

class PanelData:
    def __init__(self,
                 text='',
                 textData=None,
                 image_path='',  
                 toolTipText: Union[str, List[str], Callable] = '',
                 parent=None,
                 normal_color=None,
                 hover_color=None,
                 geo_type: Union['', GeoData] = '',
                 toolTipImagePath: Union[str, Callable] = '',
                 canDrag=True,
                 dragRect=None,
                 addToUI=True,
                 rectIsLocal=True,
                 clipRect=None,
                 name='',
                 panelType = "",
                 resizeToText: Union[tuple, bool] = False,  
                 mesh_part='',
                 after_create_fn=None
                 ):
        self.text               = text
        self.textData           = textData
        self.image_path         = image_path
        self.toolTipText        = toolTipText
        self.parent             = parent
        self.normal_color       = normal_color
        self.hover_color        = hover_color
        self.geo_type           = geo_type
        self.toolTipImagePath   = toolTipImagePath
        self.canDrag            = canDrag
        self.dragRect           = dragRect

        self.addToUI            = addToUI
        self.rectIsLocal        = rectIsLocal

        self.clipRect           = clipRect
        self.name               = name
        self.panelType          = panelType
        self.resizeToText       = resizeToText
        self.mesh_part          = mesh_part
        self.after_create_fn    = after_create_fn

    def copy(self):
        panelData = copy(self)
        panelData.textData = copy(panelData.textData)

        return panelData

    def __str__(self):
        return f"""
                text            - {self.text}
                normal_color    - {self.normal_color}
                hover_color     - {self.hover_color}
                text            - {self.text}            
                textData        - {self.textData}        
                image_path      - {self.image_path}      
                toolTipText     - {self.toolTipText}     
                parent          - {self.parent}          
                geo_type        - {self.geo_type}        
                toolTipImagePath- {self.toolTipImagePath}
                canDrag         - {self.canDrag}         
                dragRect        - {self.dragRect}     
                addToUI         - {self.addToUI}        
                rectIsLocal     - {self.rectIsLocal}
                clipRect        - {self.clipRect}       
                name            - {self.name}           
                panelType       - {self.panelType}      
                resizeToText    - {self.resizeToText}   
                mesh_part       - {self.mesh_part}      
                after_create_fn - {self.after_create_fn}

                """

    @classmethod
    def with_values(
                    cls,
                    text='',
                    textData=None,
                    image_path='',
                    toolTipText='',
                    parent=None,
                    normal_color=None,
                    hover_color=None,
                    geo_type='',
                    toolTipImagePath='',
                    canDrag=True,
                    dragRect=None,
                    addToUI=True,
                    rectIsLocal=True,
                    clipRect=None,
                    name='',
                    panelType = "",
                    resizeToText=False,
                    mesh_part = '',
                    after_create_fn=None
                    ):
        return cls(text, textData, image_path, toolTipText, parent, normal_color, hover_color, geo_type,
                   toolTipImagePath,
                   canDrag, dragRect, addToUI, rectIsLocal, clipRect, name, panelType, resizeToText, mesh_part,
                   after_create_fn)

    @classmethod
    def with_defaults(cls):
        gd = GeoData.with_defaults()
        return cls(text = '', textData = TextData.with_defaults(), image_path= gd.image_path, normal_color= gd.normal_color,
                   hover_color = gd.hover_color, geo_type = gd.geo_type)

    @classmethod
    def from_style_dict(cls, style_dict):
        gD = style_dict['geoData']
        tD = style_dict['textData']

        textData = None
        if tD:
            textData = TextData(
                tD['fontSize'],
                tD['font_id'],
                tD['align'],
                tD['color'],
            )

        if gD:
            return cls(geo_type=gD['geo_type'], normal_color=gD['normal_color'], hover_color=gD['hover_color'],
                       image_path=gD['image_path'], textData=textData)
        else:
            return cls(textData=textData)

    def merge_with_style_dict(self, style_dict):
        gD = style_dict['geoData']
        tD = style_dict['textData']

        if gD:
            if not self.normal_color:
                self.normal_color = gD['normal_color']
            if not self.hover_color:
                self.hover_color = gD['hover_color']
            if not self.image_path:
                self.image_path = gD['image_path']
            if not self.geo_type:
                self.geo_type = gD['geo_type']

        if self.textData:
            if tD:
                self.textData = TextData(
                    tD['fontSize'] if self.textData.fontSize == -1 else self.textData.fontSize,
                    tD['font_id'] if self.textData.font_id == -1 else self.textData.font_id,
                    tD['align'] if not self.textData.align else self.textData.align,
                    tD['color'] if not self.textData.color else self.textData.color
                )
            else:
                if self.text:
                    self.textData = TextData.with_defaults()

        else:
            if tD:
                self.textData = TextData(
                    tD['fontSize'],
                    tD['font_id'],
                    tD['align'],
                    tD['color']
                )
            else:
                if self.text:
                    self.textData = TextData.with_defaults()

    @staticmethod
    def apply_style(panelData: PanelData, curStyle):
        if curStyle:
            if panelData:
                styleDict = curStyle.get(panelData.panelType, None)
                if styleDict:
                    panelData.merge_with_style_dict(styleDict)
                else:
                    if panelData.panelType == 'none':
                        pass
                    else:
                        styleDict = curStyle['Panel']

                        panelData.merge_with_style_dict(styleDict)

            else:
                styleDict = curStyle['Panel']
                panelData = PanelData.from_style_dict(styleDict)
        else:
            if panelData:
                pass
            else:
                panelData = PanelData.with_defaults()
        return panelData

