
__all__ = ['GeoData']

class GeoData():
    def __init__(self,geo_type,normal_color,hover_color,image_path):
        self.geo_type       = geo_type
        self.normal_color   = normal_color
        self.hover_color    = hover_color
        self.image_path     = image_path

    def __str__(self):
        return "geoData - geo_type - {}, normal_color - {}, hover_color - {}, image_path - {}".\
            format(self.geo_type, self.normal_color,self.hover_color,self.image_path)

    @classmethod
    def with_defaults(cls, normal_color=(1,1,1,1), hover_color=None,image_path=''):
        return cls('Rect',normal_color,hover_color,image_path)
