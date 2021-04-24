from ..Geo.base_geo.Geo import Geo

from typing import Optional, NamedTuple, List,Union

class UiInfo():
    def __init__(self,index,vert_range,index_range):
        self.index: int = index
        self.vert_range: Union[list,tuple] = vert_range
        self.index_range:Union[List,tuple] = index_range

    def __str__(self):
        return f"index - {self.index}, vert_range - {self.vert_range},index_range - {self.index_range}"

    @property
    def vertCount(self):
        return self.vert_range[1] - self.vert_range[0]

    def change_info(self,indexBy:int,vrBy:int,irBy:int):
        if indexBy:
            self.index += indexBy
        if vrBy:
            self.vert_range[0] += vrBy
            self.vert_range[1] += vrBy
        if irBy:
            self.index_range[0] += irBy
            self.index_range[1] += irBy

class CombinedMeshGeo(Geo):
    def __init__(self, rectData, clipRect, geoData):
        Geo.__init__(self, clipRect, geoData)

        self.rectData   = rectData    
        self.vertices = []
        self.indices = []
        self.uvs       = []
        self.normal_colors = []
        self.hover_colors = []
        self.vertex_colors = []

        self.dict_ui_elements:List[UiInfo] = {}

    def print_ui_dict(self):
        print('***  Combined Mesh uiInfo    ***')
        for k,v in self.dict_ui_elements.items():
            print(k, v)

    def printInfo(self):
        print('***  Combined Mesh Mesh Info    ***')
        print('geo_count    - ', len(self.dict_ui_elements))
        print('vert_count   - ', len(self.vertices))
        print('uvs_count    - ', len(self.uvs))
        print('v_col_count  - ', len(self.vertex_colors))
        print('indices_count- ', len(self.indices))

        print('vertices     - ', self.vertices)
        print('uvs          - ', self.uvs)
        print('vertex_colors- ', self.vertex_colors)
        print('indices      - ', self.indices)

    def add_geometry(self,ui_element):
        if ui_element in self.dict_ui_elements:
            print(ui_element, ' already in dict_ui_elements')
            return

        ui_geo = ui_element.geo

        oldVertCount        = len(self.vertices) 
        oldIndicesCount     = len(self.indices)

        self.vertices.extend(ui_geo.vertices)

        self.indices.extend(
            list(tuple(index + oldVertCount for index in indexTuple) for indexTuple in ui_geo.indices)
        )

        if ui_geo.uvs:
            self.uvs.extend(ui_geo.uvs)

        self.normal_colors.extend(ui_geo.normal_colors)
        self.hover_colors.extend(ui_geo.hover_colors)

        self.vertex_colors = self.normal_colors

        self.dict_ui_elements[ui_element] = UiInfo(
            len(self.dict_ui_elements),  
            [oldVertCount, len(self.vertices)],
            [oldIndicesCount, len(self.indices)]
        )

    def update_uiInfo(self,ui_element,ui_index):
        print("def update_uiInfo(self,ui_element,ui_index):")
        ui_vert_cnt = len(ui_element.geo.vertices)
        ui_tris_cnt = len(ui_element.geo.indices)

        print('ui_tris_cnt - ',ui_tris_cnt)
        for i, k in enumerate(list(self.dict_ui_elements)[ui_index:]):
            print(i,k,self.dict_ui_elements[k])
            self.dict_ui_elements[k].change_info(-1,-ui_vert_cnt,-ui_tris_cnt)

    def remove_geometry(self,ui_element):
        if ui_element in self.dict_ui_elements:
            ui_element_ui_info = self.dict_ui_elements[ui_element]

            vs, ve = ui_element_ui_info.vert_range
            iNs, iNe = ui_element_ui_info.index_range
            vertCount = ui_element_ui_info.vertCount
            ui_index = ui_element_ui_info.index

            del self.vertices[vs:ve]

            self.indices = self.indices[:iNs] + list( tuple(index - vertCount for index in indexTuple) for indexTuple in self.indices[iNe:] )

            del self.normal_colors[vs:ve]
            del self.hover_colors[vs:ve]

            self.vertex_colors = self.normal_colors

            if self.uvs:
                del self.uvs[vs:ve]

            self.update_uiInfo(ui_element,ui_index)

            del self.dict_ui_elements[ui_element]

    def updateVerts(self,ui_element):
        vs,ve = self.dict_ui_elements[ui_element].vert_range

        self.vertices[vs:ve] = ui_element.geo.vertices

    def _changeColor(self,ui_element,mouseEntered):
        vs, ve = self.dict_ui_elements[ui_element].vert_range
        if mouseEntered:
            self.vertex_colors[vs:ve] = ui_element.geo.hover_colors
        else:
            self.vertex_colors[vs:ve] = ui_element.geo.normal_colors


