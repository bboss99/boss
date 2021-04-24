from enum import Enum

__all__ = ['Align','alignTuples']

alignTuples = ('Bottom', 'BL', 'Left', 'TL', 'Top', 'TR', 'Right', 'BR', 'Center')

class Align(Enum):
    Center = 0
    BL = 1
    Left = 2
    TL = 3
    Top = 4
    TR = 5
    Right = 6
    BR = 7
    Bottom = 8

    @staticmethod
    def from_str(alignStr):
        if alignStr in alignTuples:
            return getattr(Align, alignStr)
        else:
            return Align.Center


