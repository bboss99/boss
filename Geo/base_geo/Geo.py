import bgl
from gpu_extras.batch import batch_for_shader
from ... Color import Color
from ... utils import getShaderDict,json_loadPath
from os.path import dirname,join
__all__ = ['Geo']

dict_shaders = getShaderDict()

class Geo():
    def __init__(self, clipRect, geoData):
        self.clipRect           = clipRect
        self.geoData            = geoData  

        self.imageData = None  

        self._batched = None

        self.setShader()

    def setColor(self,color,whichColor = 'normal'):
        self._batched = False
        if whichColor == 'normal':
            self.normal_colors      = color if isinstance(color[0],(list,tuple)) else [color]*len(self.vertices)
            self.vertex_colors      = self.normal_colors 
        else:
            self.hover_colors       = (color if isinstance(color[0], (list, tuple)) else [color]*len(self.vertices)) if color else None

    def getColor(self,whichColor = 'normal',getList=False):
        if whichColor == 'normal':
            return self.normal_colors.copy() if getList else self.normal_colors[0]
        else:
            if self.hover_colors:
                return self.hover_colors.copy() if getList else self.hover_colors[0]
            else:
                return Color.BLACK

    def setVertexColor(self,color):
        self._batched = False
        if isinstance(color[0], (list, tuple)):
            self.vertex_colors  = color
        else:
            self.vertex_colors  = [color]*len(self.vertices)

    def setClipRect(self,clipRect):
        self.clipRect = clipRect
        self.setShader()

    def setShader(self):
        if self.geoData.image_path == '':
            if self.clipRect:
                self.shader = dict_shaders['2d_smooth_color_clip']
            else:
                self.shader = dict_shaders['2d_smooth_color']
        else:
            if self.clipRect:
                self.shader = dict_shaders['2d_image_clip']
            else:
                self.shader = dict_shaders['2d_image']
    
    def batch(self):
        if self._batched:
            return self._batched

        self._batched = self._batch()
        return self._batched

    def newbatch(self):
        self._batched = self._batch()
        return self._batched

    def _batch(self):
        if self.geoData.image_path == '':
            return batch_for_shader(
                self.shader, 'TRIS',
                {
                    "pos": self.vertices,
                    "color": self.vertex_colors
                },
                indices=self.geoData.indices,
                )
        else:
            return batch_for_shader(
                self.shader, 'TRIS',
                {
                    "pos": self.vertices,
                    "uvs": self.geoData.uvs,
                    "color": self.vertex_colors,
                },
                indices=self.geoData.indices,
                )

    def draw(self):
        batch = self._batched if self._batched else self.newbatch()

        if self.geoData.image_path == '':
            self.shader.bind()
        else:
            bgl.glActiveTexture(bgl.GL_TEXTURE0)
            bgl.glBindTexture(bgl.GL_TEXTURE_2D, self.imageData.bindcode)
            self.shader.bind()
            self.shader.uniform_int("image", 0)

        if self.clipRect:
            self.shader.uniform_float(
                'clipRect',

                self.clipRect._clipRect
            )

        batch.draw(self.shader)

    def bind_and_draw(self):
        batch = self._batched if self._batched else self.newbatch()

        if self.geoData.image_path == '':
            self.shader.bind()
        else:
            bgl.glActiveTexture(bgl.GL_TEXTURE0)
            bgl.glBindTexture(bgl.GL_TEXTURE_2D, self.imageData.bindcode)
            self.shader.bind()
            self.shader.uniform_int("image", 0)

        if self.clipRect:
            self.shader.uniform_float(
                'clipRect',

                self.clipRect._clipRect
            )

        batch.draw(self.shader)

