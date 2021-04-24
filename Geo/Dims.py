from  dataclasses import dataclass
from typing import Union

@dataclass
class DirectionLength:
    left:  Union[int,float] = 0
    right: Union[int,float] = 0
    below: Union[int,float] = 0
    above: Union[int,float] = 0

@dataclass
class HeightWidth:
    height: Union[int, float] = 0
    width: Union[int, float] = 0

@dataclass
class Point:
    x: Union[int, float] = 0
    y: Union[int, float] = 0

@dataclass
class Rect:
    bl_corner:Point
    height_width:HeightWidth
