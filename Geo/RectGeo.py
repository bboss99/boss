from copy import copy as copy_copy
from ..Geo.base_geo.Geo import Geo
from ..Geo.base_geo.GeoData import GeoData

from .. globalVars import (
                        rect_indices,
                        image_uvs,
                        rounded_rect_indices,
                        rounded_image_uvs,
                        rounded_top_rect_indices,
                        rounded_top_image_uvs,
                        rounded_bottom_rect_indices,
                        rounded_bottom_image_uvs )

__all__ = ['RectGeo','RectGeoData','RRGeoData']

class RectGeoData(GeoData):
    def __init__(self, geo_type, normal_color, hover_color, image_path='',uvs = None):
        GeoData.__init__(self, geo_type, normal_color, hover_color, image_path)
        self.indices = rect_indices
        self.uvs = uvs if uvs else image_uvs

class RRGeoData(GeoData):
    def __init__(self, geo_type, normal_color, hover_color, image_path='', pixelMargin =32, uvs = None):
        GeoData.__init__(self, geo_type, normal_color, hover_color, image_path)
        self.pixelMargin    = pixelMargin
        self.indices        = rounded_rect_indices
        self.uvs            = uvs if uvs else rounded_image_uvs

class RRTGeoData(GeoData):
    def __init__(self, geo_type, normal_color, hover_color, image_path='', pixelMargin =32, uvs = None):
        GeoData.__init__(self, geo_type, normal_color, hover_color, image_path)
        self.pixelMargin    = pixelMargin
        self.indices        = rounded_top_rect_indices
        self.uvs            = uvs if uvs else rounded_top_image_uvs

class RRBGeoData(GeoData):
    def __init__(self, geo_type, normal_color, hover_color, image_path='', pixelMargin =32, uvs = None):
        GeoData.__init__(self, geo_type, normal_color, hover_color, image_path)
        self.pixelMargin        = pixelMargin
        self.indices            = rounded_bottom_rect_indices
        self.uvs                = uvs if uvs else rounded_bottom_image_uvs

class RectGeo(Geo):
    def __init__(self,rectData,clipRect, geoData:RectGeoData):
        Geo.__init__(self,clipRect,geoData)
        self.rectData           = rectData
        
        self.vertices           = (
            (self.rectData.xMin, self.rectData.yMin), (self.rectData.xMin, self.rectData.yMax),
            (self.rectData.xMax, self.rectData.yMax), (self.rectData.xMax, self.rectData.yMin)
        )

        self.setColor(geoData.normal_color,'normal')

        self.setColor(geoData.hover_color,'hover')

    def updateVerts(self):
        self.vertices = (
            (self.rectData.xMin, self.rectData.yMin), (self.rectData.xMin, self.rectData.yMax),
            (self.rectData.xMax, self.rectData.yMax), (self.rectData.xMax, self.rectData.yMin)
        )

class RoundRectGeo(Geo):
    def __init__(self,rectData,clipRect, geoData:RRGeoData):
        Geo.__init__(self,clipRect,geoData)
        self.rectData           = rectData

        self.vertices           = self._getVerts(self.geoData.pixelMargin)
        
        self.setColor(geoData.normal_color,'normal')
        self.setColor(geoData.hover_color,'hover')
        
    def _getVerts(self,pixelMargin):
        return (
                    (self.rectData.xMin                 , self.rectData.yMin                ),
                    (self.rectData.xMin + pixelMargin   , self.rectData.yMin                ),
                    (self.rectData.xMax - pixelMargin   , self.rectData.yMin                ),
                    (self.rectData.xMax                 , self.rectData.yMin                ),
                    (self.rectData.xMin                 , self.rectData.yMin + pixelMargin  ),
                    (self.rectData.xMin + pixelMargin   , self.rectData.yMin + pixelMargin  ),
                    (self.rectData.xMax - pixelMargin   , self.rectData.yMin + pixelMargin  ),
                    (self.rectData.xMax                 , self.rectData.yMin + pixelMargin  ),
                    (self.rectData.xMin                 , self.rectData.yMax - pixelMargin  ),
                    (self.rectData.xMin + pixelMargin   , self.rectData.yMax - pixelMargin  ),
                    (self.rectData.xMax - pixelMargin   , self.rectData.yMax - pixelMargin  ),
                    (self.rectData.xMax                 , self.rectData.yMax - pixelMargin  ),
                    (self.rectData.xMin                 , self.rectData.yMax                ),
                    (self.rectData.xMin + pixelMargin   , self.rectData.yMax                ),
                    (self.rectData.xMax - pixelMargin   , self.rectData.yMax                ),
                    (self.rectData.xMax                 , self.rectData.yMax                )
            )

    def updateVerts(self):
        self.vertices = self._getVerts(self.geoData.pixelMargin)

class RoundTopRectGeo(Geo):
    def __init__(self,rectData,clipRect, geoData:RRTGeoData):
        Geo.__init__(self,clipRect,geoData)
        self.rectData           = rectData
        self.vertices           = self._getVerts(self.geoData.pixelMargin)
        
        self.setColor(geoData.normal_color,'normal')
        self.setColor(geoData.hover_color,'hover')

    def _getVerts(self,pixelMargin):
        return (
                    (self.rectData.xMin                 , self.rectData.yMin                ),
                    (self.rectData.xMin + pixelMargin   , self.rectData.yMin                ),
                    (self.rectData.xMax - pixelMargin   , self.rectData.yMin                ),
                    (self.rectData.xMax                 , self.rectData.yMin                ),
                    (self.rectData.xMin                 , self.rectData.yMax - pixelMargin  ),
                    (self.rectData.xMin + pixelMargin   , self.rectData.yMax - pixelMargin  ),
                    (self.rectData.xMax - pixelMargin   , self.rectData.yMax - pixelMargin  ),
                    (self.rectData.xMax                 , self.rectData.yMax - pixelMargin  ),
                    (self.rectData.xMin                 , self.rectData.yMax                ),
                    (self.rectData.xMin + pixelMargin   , self.rectData.yMax                ),
                    (self.rectData.xMax - pixelMargin   , self.rectData.yMax                ),
                    (self.rectData.xMax                 , self.rectData.yMax                )
        )

    def updateVerts(self):
        self.vertices = self._getVerts(self.geoData.pixelMargin)

class RoundBottomRectGeo(Geo):
    def __init__(self,rectData,clipRect, geoData:RRBGeoData):
        Geo.__init__(self,clipRect,geoData)
        self.rectData           = rectData
        self.vertices           = self._getVerts(self.geoData.pixelMargin)

        self.setColor(geoData.normal_color,'normal')
        self.setColor(geoData.hover_color,'hover')
        
    def _getVerts(self,pixelMargin):
        return (
                    (self.rectData.xMin                 , self.rectData.yMin                ),
                    (self.rectData.xMin + pixelMargin   , self.rectData.yMin                ),
                    (self.rectData.xMax - pixelMargin   , self.rectData.yMin                ),
                    (self.rectData.xMax                 , self.rectData.yMin                ),
                    (self.rectData.xMin                 , self.rectData.yMin + pixelMargin  ),
                    (self.rectData.xMin + pixelMargin   , self.rectData.yMin + pixelMargin  ),
                    (self.rectData.xMax - pixelMargin   , self.rectData.yMin + pixelMargin  ),
                    (self.rectData.xMax                 , self.rectData.yMin + pixelMargin  ),
                    (self.rectData.xMin                 , self.rectData.yMax                ),
                    (self.rectData.xMin + pixelMargin   , self.rectData.yMax                ),
                    (self.rectData.xMax - pixelMargin   , self.rectData.yMax                ),
                    (self.rectData.xMax                 , self.rectData.yMax                )
        )

    def updateVerts(self):
        self.vertices = self._getVerts(self.geoData.pixelMargin)

