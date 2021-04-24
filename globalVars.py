from dataclasses import dataclass
from typing import Union

ui_types                   = (
    'Panel','Button','CheckBox','ColorField',
    'DropDownBox','TextField','FloatField','IntField',
    'VectorFloatField','VectorIntField','VectorBooleanField',
    'Slider','Slider2',

)

geo_types                  = ('Rect','RR','RRT','RRB','CIR')
image_uvs                  = ((0, 0), (0, 1), (1, 1), (1, 0))
image_uvs_flipped          = ((1, 0), (1, 1), (0, 1), (0, 0))

rect_indices               = ((0, 1, 2), (0, 2, 3))

rounded_image_uvs            = (
                            ( 0 , 0),
                            (.5 , 0),
                            (.5 , 0),
                            ( 1 , 0),
                            ( 0 ,.5),
                            (.5 ,.5),
                            (.5 ,.5),
                            ( 1 ,.5),
                            ( 0 ,.5),
                            (.5 ,.5),
                            (.5 ,.5),
                            ( 1 ,.5),
                            ( 0 , 1),
                            (.5 , 1),
                            (.5 , 1),
                            ( 1 , 1)
                            )

rounded_rect_indices       = (
                                (0  , 4  , 5), 
                                (0  , 5  , 1),
                                (1  , 5  , 6),
                                (1  , 6  , 2),
                                (2  , 6  , 7),
                                (2  , 7  , 3),
                                (4  , 8  , 9),
                                (4  , 9  , 5),
                                (5  , 9  ,10),
                                (5  ,10  , 6),
                                (6  ,10  ,11),
                                (6  ,11  , 7),
                                (8  ,12  ,13),
                                (8  ,13  , 9),
                                (9  ,13  ,14),
                                (9  ,14  ,10),
                                (10 ,14  ,15),
                                (10 ,15  ,11)
                                )

rounded_top_image_uvs        = (
                                ( 0 ,.5),
                                (.5 ,.5),
                                (.5 ,.5),
                                ( 1 ,.5),
                                ( 0 ,.5),
                                (.5 ,.5),
                                (.5 ,.5),
                                ( 1 ,.5),
                                ( 0 , 1),
                                (.5 , 1),
                                (.5 , 1),
                                ( 1 , 1)
                                )

rounded_top_rect_indices   = (
                                (0  , 4  , 5), 
                                (0  , 5  , 1),
                                (1  , 5  , 6),
                                (1  , 6  , 2),
                                (2  , 6  , 7),
                                (2  , 7  , 3),
                                (4  , 8  , 9),
                                (4  , 9  , 5),
                                (5  , 9  ,10),
                                (5  ,10  , 6),
                                (6  ,10  ,11),
                                (6  ,11  , 7)
                                )
    
rounded_bottom_image_uvs        = (
                                    ( 0 , 0),
                                    (.5 , 0),
                                    (.5 , 0),
                                    ( 1 , 0),
                                    ( 0 ,.5),
                                    (.5 ,.5),
                                    (.5 ,.5),
                                    ( 1 ,.5),
                                    ( 0 ,.5),
                                    (.5 ,.5),
                                    (.5 ,.5),
                                    ( 1 ,.5),
                                )

rounded_bottom_rect_indices   = (
                                    (0  , 4  , 5), 
                                    (0  , 5  , 1),
                                    (1  , 5  , 6),
                                    (1  , 6  , 2),
                                    (2  , 6  , 7),
                                    (2  , 7  , 3),
                                    (4  , 8  , 9),
                                    (4  , 9  , 5),
                                    (5  , 9  ,10),
                                    (5  ,10  , 6),
                                    (6  ,10  ,11),
                                    (6  ,11  , 7)
                                )
          

