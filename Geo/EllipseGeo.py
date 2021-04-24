from .. Geo.base_geo.GeoData import GeoData
from .. Geo.base_geo.Geo import Geo

from .. math.Vector2D import rotate_point

__all__ = ['EllipseGeoData','EllipseGeo']

class EllipseGeoData(GeoData):
    def __init__(self,geo_type,normal_color, hover_color, image_path = '',pointCount = 16):
        GeoData.__init__(self, geo_type,normal_color, hover_color,image_path )
        self.pointCount = pointCount
        self.indices = self.get_indices()

    def get_indices(self):
        indices = [(0, i + 1, i + 2) for i in range(self.pointCount - 1)]

        indices.append((0, self.pointCount, 1))
        return indices

    @classmethod
    def from_pointCount(cls, normal_color, hover_color, image_path = '',pointCount = 16):
        return cls('CIR',normal_color, hover_color, image_path,pointCount)

    @classmethod
    def with_defaults(cls, normal_color=(1,1,1,1), hover_color=None,image_path='',pointCount = 16):
        return cls('CIR',normal_color,hover_color,image_path,pointCount)

class EllipseGeo(Geo):
    def __init__(self,rectData,clipRect, ellipseGeoData):
        Geo.__init__(self,clipRect,ellipseGeoData)
        self.rectData           = rectData
        
        self.pointCount         = ellipseGeoData.pointCount

        self.center             = self.getCenter()
        
        self.setFirstPoint()

        self.setRadius() 
        
        self.rectData.add_onUpdate(self.setRadius)

        self.vertices           = self._getVerts()
        
        self.setColor(ellipseGeoData.normal_color,'normal')
        self.setColor(ellipseGeoData.hover_color,'hover')
        
    def setRadius(self):
        self.radius             = (self.rectData.yMax - self.rectData.yMin)/2

    def getCenter(self):
        return (
                (self.rectData.xMin + self.rectData.xMax)/2,
                (self.rectData.yMin + self.rectData.yMax)/2
               )
    
    def setFirstPoint(self):
        self.firstPoint = ((self.rectData.xMin + self.rectData.xMax)/2, self.rectData.yMin)

    def _getVerts(self):
        rotateByAngle = 360 / self.pointCount  
        return [self.center] + [rotate_point(self.center,self.firstPoint,rotateByAngle*i) for i in range(self.pointCount)]
    
    def recalculateVerts(self):
        self.setFirstPoint()
        self.vertices = self._getVerts()

    def updateVerts(self):
        self.center             = self.getCenter()

        prevCenter              = self.vertices[0]

        diff                    = ( self.center[0] - prevCenter[0], self.center[1] - prevCenter[1] )

        newVerts = []        
        for each in self.vertices:
            newVerts.append ( ( each[0] +  diff[0],each[1] + diff[1]) )
        
        self.vertices = newVerts


